%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-sdk-kms

Name: rubygem-aws-sdk-kms
Version:        1.77.0
Release:        1%{?dist}
Summary:        Official AWS Ruby gem for AWS Key Management Service (KMS).
Group:          Development/Languages
License:        Apache 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/aws-sdk-kms-%{version}.gem
%define sha512    aws-sdk-kms=1057c29c5c489b06f411f4bf3744c0b3088d0d72897cc202600b99efbaffd6058a15aa7cc41ce08f8a767e05277711028401cc0b16eac4b0960bfeacc8929d27
BuildRequires:  ruby

Requires: rubygem-aws-sdk-core >= 3
Requires: rubygem-aws-sigv4 >= 1.0

%description
Official AWS Ruby gem for AWS Key Management Service (KMS).
This gem is part of the AWS SDK for Ruby.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.77.0-1
-   Update to version 1.77.0
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.59.0-1
-   Automatic Version Bump
*   Wed Sep 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.39.0-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.38.0-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.37.0-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.9.0-1
-   Update to version 1.9.0
*   Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.6.0-1
-   Initial build
