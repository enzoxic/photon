%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name trollop
Name:           rubygem-trollop
Version:        2.9.10
Release:        2%{?dist}
Summary:        Commandline option parser for Ruby
Group:          Applications/Programming
License:        BSD
Vendor:         VMware, Inc.
Distribution:   Photon
URL: https://rubygems.org/gems/%{gem_name}
Source0: https://rubygems.org/downloads/trollop-%{version}.gem
%define sha512 trollop=21a0db09d480353ff846a1311b118e0b0db4ca13a559dd1749c1478eff7080dd04e5308dbf1807215eadb68e276c991970b23357e9a3497acb9f705f7f77253c

BuildRequires: ruby

Requires: ruby

%description
Commandline option parser for Ruby

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.9.10-2
- Bump Version to build with new ruby
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.9.10-1
- Automatic Version Bump
* Tue Nov 27 2018 Sujay G <gsujay@vmware.com> 2.9.9-2
- Added %check section
* Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 2.9.9-1
- Update to version 2.9.9
* Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 2.1.2-3
- Bump up release number to reflect ruby upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.2-2
- GA - Bump release of all rpms
* Wed Nov 11 2015 Alexey Makhalov <amakhalov@vmware.com> 2.1.2-1
- Initial build
