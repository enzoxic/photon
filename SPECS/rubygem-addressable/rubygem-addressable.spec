%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name addressable

Name:           rubygem-addressable
Version:        2.8.6
Release:        1%{?dist}
Summary:        An easy-to-use client library for making requests from Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache-2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  addressable=a7cb784cd5564cabec99eb7582ac17969b166e38057c23f3df74707d0078d00d001c2523432ce4e52720528ee808f314f2d6c9139562de27b599363b919cca65

BuildRequires:  ruby >= 2.0.0

Requires:       rubygem-public_suffix >= 2.0.2, rubygem-public_suffix < 6.0

BuildArch: noarch

%description
Addressable is a replacement for the URI implementation that is part of Ruby's standard library.
It more closely conforms to the relevant RFCs and adds support for IRIs and URI templates.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.8.6-1
-   Update to version 2.8.6
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.8.1-1
-   Automatic Version Bump
*   Tue Sep 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.7.0-2
-   Update rubygem-public_suffix version
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.7.0-1
-   Automatic Version Bump
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.6.0-1
-   Initial build
