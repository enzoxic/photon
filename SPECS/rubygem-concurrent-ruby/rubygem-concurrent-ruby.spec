%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name concurrent-ruby

Name: rubygem-concurrent-ruby
Version:        1.2.3
Release:        1%{?dist}
Summary:        Modern concurrency tools for Rails framework.
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/concurrent-ruby/versions/%{version}
Source0:        https://rubygems.org/downloads/concurrent-ruby-%{version}.gem
%define sha512    concurrent-ruby=644696300373709f2ed0c76a7abbfb989f2325578ebf92c3536419cf8e25b2defab251d60fd9f0ad6f9d79e102baac6578de4f2822d9cb0cf571ed2f7a05b9ea
BuildRequires:  ruby

%description
Modern concurrency tools including agents, futures, promises, thread pools, actors,
supervisors, and more. Inspired by Erlang, Clojure, Go, JavaScript, actors, and
classic concurrency patterns.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.2.3-1
-   Update to version 1.2.3
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.1.10-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.7-1
-   Automatic Version Bump
*   Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.5-1
-   Initial build
