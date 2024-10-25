%global debug_package   %{nil}
%define plugins_dir     %{_libexecdir}/docker/cli-plugins

Name:           docker-compose
Version:        2.26.1
Release:        5%{?dist}
Summary:        Multi-container orchestration for Docker
Group:          Application/File
Vendor:         VMware, Inc.
Distribution:   Photon
License:        ASL 2.0
URL:            https://github.com/docker/compose
Source0:        https://github.com/docker/compose/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%define sha512  %{name}=4a97326c6ed974400aca91a64e93ef0e1fa6b52f988f636b8bbcb43e14442c6702e2d42afda3e491a9da18176448f342ebae7212bf59617372295d831beb8aba

BuildRequires:  go
BuildRequires:  ca-certificates

%description
Docker Compose (V2) plugin for the Docker CLI.

This plugin provides the 'docker compose' subcommand.

The binary can also be run standalone as a direct replacement for
Docker Compose V1 ('docker-compose').

%prep
%autosetup -p1 -n compose-%{version}

%build
%make_build VERSION=%{version} build

%install
install -D -p -m 0755 ./bin/build/%{name} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{plugins_dir}
ln -srv %{buildroot}%{_bindir}/%{name} %{buildroot}%{plugins_dir}/

for f in LICENSE MAINTAINERS NOTICE README.md; do
    install -D -p -m 0644 "$f" "%{name}-docs/$f"
done

%check
ver="$(%{buildroot}%{_bindir}/%{name} docker-cli-plugin-metadata | awk '{ gsub(/[",:]/,"")}; $1 == "Version" { print $2 }')"; \
    test "$ver" = %{version} && echo "PASS: %{name} version OK" || (echo "FAIL: %{name} version ($ver) did not match" && exit 1)

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{name}-docs/*
%{_bindir}/%{name}
%{plugins_dir}/%{name}

%changelog
* Fri Oct 25 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.26.1-5
- Create a sym link to make `docker compose` work.
* Thu Sep 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.26.1-4
- Bump version as a part of go upgrade
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.26.1-3
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 2.26.1-2
- Bump version as a part of go upgrade
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 2.26.1-1
- Version upgrade to resolve second level CVEs
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.2-3
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.2-2
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.20.2-1
- Upgrade to 2.20.2.
* Fri Jun 23 2023 Piyush Gupta <gpiyush@vmware.com> 2.19.0-1
- Upgrade to v2.19.0.
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 2.11.0-7
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.11.0-6
- Bump up version to compile with new go
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 2.11.0-5
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 2.11.0-4
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 2.11.0-3
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 2.11.0-2
- Bump up version to compile with new go
* Mon Sep 19 2022 Mukul Sikka <msikka@vmware.com> 2.11.0-1
- Initial Build
