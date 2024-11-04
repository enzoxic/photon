Name:           ninja-build
Summary:        Small build system with focus on speed
Version:        1.11.1
Release:        2%{?dist}
URL:            https://ninja-build.org
Vendor:         VMware, Inc.
Group:          Development/Tools
Distribution:   Photon

Source0: https://github.com/ninja-build/ninja/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=1bca38877c70ee6613f347ffccef5adc02ba0a3947c62ae004ea97f918442b5a3de92378e4f820ae2a7676bc7609d25fbc7d41f6cfb3a61e5e4b26ec3639e403

Source1:        macros.ninja
Source2: license.txt
%include %{SOURCE2}

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
%autosetup -n ninja-%{version} -p1

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
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.11.1-2
- Release bump for SRP compliance
* Wed Jan 04 2023 Susant Sahani <ssahani@vmware.com> 1.11.1-1
- Version Bump
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.11.0-2
- Update release to compile with python 3.11
* Tue Aug 30 2022 Susant Sahani <ssahani@vmware.com> 1.11.0-1
- Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.10.1-1
- Automatic Version Bump
* Fri May 08 2020 Susant Sahani<ssahani@vmware.com> 1.10.0-1
- Update to 1.10.0
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8.2-2
- Cross compilation support
* Wed Dec 27 2017 Anish Swaminathan <anishs@vmware.com> 1.8.2-1
- Initial packaging
