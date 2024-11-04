Summary:        Libcap
Name:           libcap
Version:        2.66
Release:        3%{?dist}
URL:            https://www.gnu.org/software/hurd/community/gsoc/project_ideas/libcap.html
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.xz
%define sha512  libcap=ac005b622f6e065f30ce282a5c87240e7b9da75366ee537aa4835bc501b44bc242c10a4ba4dc070e2415fc7f635d1c3c4e45fbeeaf962cf7973dda82bf6377f0

Source1: license.txt
%include %{SOURCE1}

Patch0:         CVE-2023-2602.patch
Patch1:         CVE-2023-2603.patch

%description
The libcap package implements the user-space interfaces to the POSIX 1003.1e capabilities available in Linux kernels.
These capabilities are a partitioning of the all powerful root privilege into a set of distinct privileges.

%package        devel
Summary:        Development files for libcap
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The libcap-devel package contains libraries, header files and documentation for developing applications that use libcap.

%prep
%autosetup -p1

%build
if [ %{_host} != %{_build} ]; then
  MFLAGS="CC=%{_arch}-unknown-linux-gnu-gcc AR=%{_arch}-unknown-linux-gnu-ar RANLIB=%{_arch}-unknown-linux-gnu-ranlib BUILD_CC=gcc"
else
  MFLAGS=
fi
sed -i 's:LIBDIR:PAM_&:g' pam_cap/Makefile
make %{?_smp_mflags} $MFLAGS

%install
make prefix=%{_prefix} \
     SBINDIR=%{_sbindir} \
     PAM_LIBDIR=%{_libdir} \
     RAISE_SETFCAP=no \
     DESTDIR=%{buildroot} \
     %{?_smp_mflags} \
     install
%ifarch aarch64
test -d %{buildroot}%{_libdir} && mv %{buildroot}%{_libdir} %{buildroot}%{_lib64dir}
%endif
chmod -v 755 %{buildroot}/usr/lib64/libcap.so

%check
cd progs
sed -i "s|pass_capsh --chroot=\$(/bin/pwd) ==||g" quicktest.sh
./quicktest.sh

%files
%defattr(-,root,root)
%{_lib64dir}/libcap.so.*
%{_lib64dir}/libpsx.so.*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%exclude %{_lib64dir}/libcap.a
%exclude %{_lib64dir}/libpsx.a
%{_lib64dir}/pkgconfig/*
%{_lib64dir}/libcap.so
%{_lib64dir}/libpsx.so
%{_mandir}/man3/*

%changelog
*   Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.66-3
-   Release bump for SRP compliance
*   Fri Jun 02 2023 Piyush Gupta <gpiyush@vmware.com> 2.66-2
-   Fix CVE-2023-2602, CVE-2023-2603.
*   Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 2.66-1
-   Automatic Version Bump
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.64-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.49-1
-   Automatic Version Bump
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 2.43-1
-   Automatic Version Bump
*   Wed Jul 29 2020 Tapas Kundu <tkundu@vmware.com> 2.31-1
-   Update to 2.31
*   Tue Nov 26 2019 Alexey Makhalov <amakhalov@vmware.com> 2.25-9
-   Cross compilation support
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.25-8
-   Aarch64 support
*   Wed Aug 09 2017 Danut Moraru <dmoraru@vmware.com> 2.25-7
-   Remove capsh test that runs chroot already in chroot, failing due to
    expected environment/dependencies not available
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.25-6
-   Remove attr deps.
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.25-5
-   Moved man3 to devel subpackage.
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2.25-4
-   BuildRequired attr-devel.
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.25-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.25-2
-   GA - Bump release of all rpms
*   Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com> 2.25-1
-   Updating Version.
*   Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 2.24-2
-   Moving static lib files to devel package.
*   Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 2.24-1
-   Initial version.
