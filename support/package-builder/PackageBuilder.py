#!/usr/bin/env python3

import os
import sys

from PackageUtils import PackageUtils
from Logger import Logger
from ToolChainUtils import ToolChainUtils
from CommandUtils import CommandUtils
from constants import constants
from SpecData import SPECS
from StringUtils import StringUtils
from Sandbox import Chroot, SystemdNspawn, Container
from SRP import SRP


class PackageBuilder(object):
    def __init__(self, pkg, mapPackageToCycles, sandboxType):
        # will be initialized in buildPackageFunction()
        self.package, self.version = StringUtils.splitPackageNameAndVersion(pkg)
        self.mapPackageToCycles = mapPackageToCycles
        self.logName = f"build-{pkg}"
        self.logPath = os.path.join(constants.logPath, f"{pkg}.{constants.currentArch}")
        # Cleanup the log directory
        os.makedirs(self.logPath, exist_ok=True)
        CommandUtils.runCmd(["find", self.logPath, "-name", "*.log", "-delete"])
        self.logger = Logger.getLogger(self.logName, self.logPath, constants.logLevel)
        self.listNodepsPackages = [
            "glibc",
            "gmp",
            "zlib",
            "file",
            "binutils",
            "mpfr",
            "mpc",
            "gcc",
            "ncurses",
            "util-linux",
            "groff",
            "perl",
            "texinfo",
            "rpm",
            "openssl",
            "go",
        ]

        self.srp = SRP(pkg, self.logger)
        if sandboxType == "chroot":
            self.sandbox = Chroot(pkg, self.logger, self.srpLogCommand)
        elif sandboxType == "systemd-nspawn":
            self.sandbox = SystemdNspawn(pkg, self.logger, self.srpLogCommand)
        elif sandboxType == "container":
            self.sandbox = Container(pkg, self.logger, self.srpLogCommand)
        else:
            raise Exception("Unknown sandbox type: " + sandboxType)

    def build(self, doneList):
        # do not build if RPM is already built
        # test only if the package is in the testForceRPMS with rpmCheck
        # build only if the package is not in the testForceRPMS with rpmCheck
        if not (constants.rpmCheck or self.package in constants.testForceRPMS):
            if self._checkIfPackageIsAlreadyBuilt(self.package, self.version, doneList):
                return

        try:
            self._buildPackage(doneList)
        except Exception as e:
            # TODO: self.logger might be None
            self.logger.exception(e)
            raise e

    def _buildPackage(self, doneList):
        try:
            self.srp.initialize()
            self.sandbox.create()

            tUtils = ToolChainUtils(self.logName, self.logPath, self.srpLogCommand)
            if self.sandbox.hasToolchain():
                inputRPMS = tUtils.installExtraToolchainRPMS(
                    self.sandbox, self.package, self.version
                )
            else:
                inputRPMS = tUtils.installToolchainRPMS(
                    self.sandbox, self.package, self.version, availablePackages=doneList
                )
            self.srp.addInputRPMS(inputRPMS)

            if (self.package not in constants.listCoreToolChainPackages) or (
                constants.rpmCheck and self.package in constants.testForceRPMS
            ):
                self._installDependencies(constants.buildArch)
                if constants.crossCompiling:
                    self._installDependencies(constants.targetArch)

            pkgUtils = PackageUtils(self.logName, self.logPath)
            for _, v in constants.CopyToSandboxDict.items():
                pkgUtils.copyFileToSandbox(self.sandbox, v["src"], v["dest"])
            pkgUtils.adjustGCCSpecs(self.sandbox, self.package, self.version)
            listRPMFiles, listSRPMFiles = pkgUtils.buildRPMSForGivenPackage(
                self.sandbox, self.package, self.version, self.logPath
            )
            self.srp.addObservation(self.sandbox.getObservation())
            self.srp.addOutputRPMS(listRPMFiles + listSRPMFiles)
            self.logger.debug(f"Successfully built the package: {self.package}")
        except Exception as e:
            self.logger.error(f"Failed while building package: {self.package}")
            self.logger.debug(
                f"Sandbox: {self.sandbox.name} not deleted for debugging."
            )
            if constants.rpmCheck and self.package in constants.testForceRPMS:
                logFileName = os.path.join(self.logPath, f"{self.package}-test.log")
            else:
                logFileName = os.path.join(self.logPath, f"{self.package}.log")
            CommandUtils.runCmd(
                ["tail", "-n", "100", logFileName],
                ignore_rc=True,
                logfn=self.logger.info,
            )
            self.logger.exception(e)
            raise
        self.sandbox.destroy()
        self.srp.finalize()

    def _installDependencies(self, arch, deps=[]):
        (
            listDependentPackages,
            listTestPackages,
            listInstalledPackages,
            listInstalledRPMs,
        ) = self._findDependentPackagesAndInstalledRPM(self.sandbox, arch)

        # PackageUtils should be initialized here - as per arch basis
        # Do not move it to __init__
        pkgUtils = PackageUtils(self.logName, self.logPath)

        if listDependentPackages:
            self.logger.debug(
                "Installing the build time dependent packages for " + arch
            )
            for pkg in listDependentPackages:
                packageName, packageVersion = StringUtils.splitPackageNameAndVersion(
                    pkg
                )
                self._installPackage(
                    pkgUtils,
                    packageName,
                    packageVersion,
                    self.sandbox,
                    self.logPath,
                    listInstalledPackages,
                    listInstalledRPMs,
                    arch,
                )
            for pkg in listTestPackages:
                flag = False
                packageName, packageVersion = StringUtils.splitPackageNameAndVersion(
                    pkg
                )
                for depPkg in listDependentPackages:
                    depPackageName, depPackageVersion = (
                        StringUtils.splitPackageNameAndVersion(depPkg)
                    )
                    if depPackageName == packageName:
                        flag = True
                        break
                if flag == False:
                    self._installPackage(
                        pkgUtils,
                        packageName,
                        packageVersion,
                        self.sandbox,
                        self.logPath,
                        listInstalledPackages,
                        listInstalledRPMs,
                        arch,
                    )
            pkgUtils.installRPMSInOneShot(self.sandbox, arch)
            self.logger.debug(
                "Finished installing the build time dependent packages for " + arch
            )

    def srpLogCommand(self, cmd, env={}):
        self.srp.addCommand(cmd, env)

    def _findPackageNameAndVersionFromRPMFile(self, rpmfile):
        rpmfile = os.path.basename(rpmfile)
        releaseindex = rpmfile.rfind("-")
        if releaseindex == -1:
            self.logger.error("Invalid rpm file:" + rpmfile)
            return None
        pkg = rpmfile[0:releaseindex]
        return pkg

    def _findInstalledPackages(self, sandbox, arch):
        pkgUtils = PackageUtils(self.logName, self.logPath)
        listInstalledRPMs = pkgUtils.findInstalledRPMPackages(sandbox, arch)
        listInstalledPackages = []
        for installedRPM in listInstalledRPMs:
            pkg = self._findPackageNameAndVersionFromRPMFile(installedRPM)
            if pkg is not None:
                listInstalledPackages.append(pkg)
        return listInstalledPackages, listInstalledRPMs

    def _checkIfPackageIsAlreadyBuilt(self, package, version, doneList):
        basePkg = SPECS.getData().getSpecName(package) + "-" + version
        return basePkg in doneList

    def _findRunTimeRequiredRPMPackages(self, rpmPackage, version, arch):
        return SPECS.getData(arch).getRequiresForPackage(rpmPackage, version)

    def _findBuildTimeRequiredPackages(self, arch):
        deps = SPECS.getData(arch).getBuildRequiresForPackage(
            self.package, self.version
        )

        # Add BuildRequiresNative list
        if constants.crossCompiling and arch == constants.buildArch:
            deps.extend(
                SPECS.getData(arch).getBuildRequiresNativeForPackage(
                    self.package, self.version
                )
            )

        return deps

    def _findBuildTimeCheckRequiredPackages(self):
        return SPECS.getData().getCheckBuildRequiresForPackage(
            self.package, self.version
        )

    def _installPackage(
        self,
        pkgUtils,
        package,
        packageVersion,
        sandbox,
        destLogPath,
        listInstalledPackages,
        listInstalledRPMs,
        arch,
    ):
        rpmfile = pkgUtils.findRPMFile(package, packageVersion, arch)
        if rpmfile is None:
            self.logger.error(
                "No rpm file found for package: " + package + "-" + packageVersion
            )
            raise Exception("Missing rpm file")
        specificRPM = os.path.basename(rpmfile.replace(".rpm", ""))
        pkg = self._findPackageNameAndVersionFromRPMFile(f"{package}-{packageVersion}")
        if pkg in listInstalledPackages:
            return
        # mark it as installed -  to avoid recursion
        listInstalledPackages.append(pkg)
        listInstalledRPMs.append(specificRPM)
        self._installDependentRunTimePackages(
            pkgUtils,
            package,
            packageVersion,
            sandbox,
            destLogPath,
            listInstalledPackages,
            listInstalledRPMs,
            arch,
        )
        noDeps = False
        if (
            package in self.mapPackageToCycles
            or package in self.listNodepsPackages
            or package in constants.noDepsPackageList
        ):
            noDeps = True
        pkgUtils.prepRPMforInstall(package, packageVersion, noDeps, destLogPath, arch)

    def _installDependentRunTimePackages(
        self,
        pkgUtils,
        package,
        packageVersion,
        sandbox,
        destLogPath,
        listInstalledPackages,
        listInstalledRPMs,
        arch,
    ):
        listRunTimeDependentPackages = self._findRunTimeRequiredRPMPackages(
            package, packageVersion, arch
        )
        if listRunTimeDependentPackages:
            for pkg in listRunTimeDependentPackages:
                if pkg in self.mapPackageToCycles:
                    continue
                packageName, packageVersion = StringUtils.splitPackageNameAndVersion(
                    pkg
                )
                rpmfile = pkgUtils.findRPMFile(packageName, packageVersion, arch, True)
                if rpmfile is None:
                    self.logger.error(
                        "No rpm file found for package: "
                        + packageName
                        + "-"
                        + packageVersion
                    )
                    raise Exception("Missing rpm file")
                latestPkgRPM = os.path.basename(rpmfile).replace(".rpm", "")
                if pkg in listInstalledPackages and latestPkgRPM in listInstalledRPMs:
                    continue
                self._installPackage(
                    pkgUtils,
                    packageName,
                    packageVersion,
                    sandbox,
                    destLogPath,
                    listInstalledPackages,
                    listInstalledRPMs,
                    arch,
                )

    def _findDependentPackagesAndInstalledRPM(self, sandbox, arch):
        listInstalledPackages, listInstalledRPMs = self._findInstalledPackages(
            sandbox, arch
        )
        self.logger.debug(listInstalledPackages)
        if constants.crossCompiling and arch == constants.buildArch:
            listDependentPackages = self._findBuildTimeRequiredPackages(
                constants.targetArch
            )
            # TODO remove unsupported by buildArch packages from this list
        else:
            listDependentPackages = self._findBuildTimeRequiredPackages(arch)
        listTestPackages = []
        if constants.rpmCheck and self.package in constants.testForceRPMS:
            # One time optimization
            if constants.listMakeCheckRPMPkgWithVersionstoInstall is None:
                constants.listMakeCheckRPMPkgWithVersionstoInstall = []
                for package in constants.listMakeCheckRPMPkgtoInstall:
                    version = SPECS.getData(arch).getHighestVersion(package)
                    constants.listMakeCheckRPMPkgWithVersionstoInstall.append(
                        package + "-" + version
                    )

            listDependentPackages.extend(self._findBuildTimeCheckRequiredPackages())
            testPackages = (
                set(constants.listMakeCheckRPMPkgWithVersionstoInstall)
                - set(listInstalledPackages)
                - set([self.package + "-" + self.version])
            )
            listTestPackages = list(set(testPackages))
            listDependentPackages = list(set(listDependentPackages))
        return (
            listDependentPackages,
            listTestPackages,
            listInstalledPackages,
            listInstalledRPMs,
        )
