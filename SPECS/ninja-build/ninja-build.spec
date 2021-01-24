Name:           ninja-build
Summary:        Small build system with focus on speed
Version:        1.10.2
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://ninja-build.org
Vendor:         VMware, Inc.
Group:          Development/Tools
Distribution:   Photon
Source0:        https://github.com/ninja-build/ninja/archive/%{name}-%{version}.tar.gz
%define sha1    ninja-build=8d2e8c1c070c27fb9dc46b4a6345bbb1de7ccbaf
Source1:        macros.ninja

BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  gtest-devel

%description
Ninja is a small build system with a focus on speed.
It differs from other build systems in two major respects:
it is designed to have its input files generated by a
higher-level build system, and it is designed to run builds
as fast as possible.

%prep
%setup -n ninja-%{version}

%build

python3 configure.py --bootstrap --verbose
if [ %{_host} != %{_build} ]; then
  sed -i 's/cxx = g++/cxx = %{_host}-g++/' build.ninja
fi
./ninja -v all

%install
install -Dpm0755 ninja -t %{buildroot}%{_bindir}/
install -Dpm0644 misc/bash-completion %{buildroot}%{_datadir}/bash-completion/completions/ninja
install -Dpm0644 %{SOURCE1} %{buildroot}%{_libdir}/rpm/macros.d/macros.ninja

%check
./ninja_test --gtest_filter=-SubprocessTest.SetWithLots

%files
%license COPYING
%{_bindir}/ninja
%{_datadir}/bash-completion/completions/ninja
%{_libdir}/rpm/macros.d/macros.ninja

%changelog
*   Sat Jan 23 2021 Susant Sahani <ssahani@vmware.com> 1.10.2-1
-   Automatic Version Bump
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.10.1-1
-   Automatic Version Bump
*   Fri May 08 2020 Susant Sahani<ssahani@vmware.com> 1.10.0-1
-   Update to 1.10.0
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8.2-2
-   Cross compilation support
*   Wed Dec 27 2017 Anish Swaminathan <anishs@vmware.com> 1.8.2-1
-   Initial packaging
