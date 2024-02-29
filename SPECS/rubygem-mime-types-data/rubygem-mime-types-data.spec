%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name mime-types-data

Name: rubygem-mime-types-data
Version:        3.2024.0206
Release:        1%{?dist}
Summary:        Provides a registry for information about MIME media type definitions.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512    mime-types-data=765c8671ec68b2c43f0f9a91da455e7d7533ec85a40f2b251861b0b0eab992dcdd3cbd2bc81631f447d683e1ca38b42e2724af40d437939736aa29170b395c13
BuildRequires:  ruby >= 2.0

BuildArch: noarch

%description
mime-types-data provides a registry for information about MIME media type definitions.
It can be used with the Ruby mime-types library or other software to determine defined
filename extensions for MIME types, or to use filename extensions to look up the likely
MIME type definitions.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.2024.0206-1
-   Update to version 3.2024.0206
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2022.0105-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 3.2020.0512-1
-   Automatic Version Bump
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.2015.1120-1
-   Initial build
