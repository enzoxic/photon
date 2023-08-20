%define srcname sphinxcontrib-serializinghtml

Name:           python3-sphinxcontrib-serializinghtml
Version:        1.1.4
Release:        3%{?dist}
Summary:        Sphinx extension for serialized HTML
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/sphinxcontrib-serializinghtml

Source0: https://files.pythonhosted.org/packages/ac/86/021876a9dd4eac9dae0b1d454d848acbd56d5574d350d0f835043b5ac2cd/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=d132f75f1e0491167cd6d0f5b3697ac0fc1b16e63fd3dcd480b961e332b521932e405679a695522a4aeb56f57949eb9b1ed7635e9807dd059ae44a6384bdc6d0

BuildArch: noarch

BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-setuptools

Requires: python3

Provides: python%{python3_version}dist(%{srcname})

%description
sphinxcontrib-serializinghtml is a sphinx extension which outputs "serialized"
HTML files (json and pickle).

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%license LICENSE
%doc README.rst

%changelog
* Sun Aug 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.4-3
- Fix summary & description
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.1.4-2
- Update release to compile with python 3.10
* Mon Dec 14 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.1.4-1
- initial version
