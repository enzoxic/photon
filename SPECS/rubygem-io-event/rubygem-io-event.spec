%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name io-event
%global ruby_ver 3.3.0

Name:           rubygem-io-event
Version:        1.4.4
Release:        1%{?dist}
Summary:        An event loop.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=8a11aecb9019a2154110b900e99fe19325daa554d15a60261093b56edae9c23ceec4d54616cd11be4a5dede5e73c4bba144d40621e80ad2203a3d2261f06d178

BuildRequires:  ruby

Requires: ruby

BuildArch: noarch

%description
Provides low level cross-platform primitives for constructing
event loops, with support for select, kqueue, epoll and io_uring.

%prep
gem unpack %{SOURCE0}
%autosetup -p1 -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
gem install %{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}%{gemdir}/cache
mkdir -p %{buildroot}%{gemdir}/doc
mkdir -p %{buildroot}%{gemdir}/plugins
mkdir -p %{buildroot}%{gemdir}/specifications
mkdir -p %{buildroot}%{gemdir}/gems
mkdir -p %{buildroot}%{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}
cp -pa %{gemdir}/build_info %{buildroot}%{gemdir}/
cp -pa %{gemdir}/cache/%{gem_name}-%{version}.gem %{buildroot}%{gemdir}/cache/
cp -pa %{gemdir}/doc/%{gem_name}-%{version} %{buildroot}%{gemdir}/doc/
cp -pa %{gemdir}/plugins %{buildroot}%{gemdir}/
cp -pa %{gemdir}/specifications/%{gem_name}-%{version}.gemspec %{buildroot}%{gemdir}/specifications
cp -pa %{gemdir}/gems/%{gem_name}-%{version} %{buildroot}%{gemdir}/gems
cp -pa %{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}/%{gem_name}-%{version} %{buildroot}%{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.4-1
- Update to version 1.4.4
* Wed Oct 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-1
- Initial version. Needed by fiber-local.
