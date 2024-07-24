%define srcname             setuptools
%define python_wheel_dir    %{_datadir}/python-wheels
%define python_wheel_name   %{srcname}-%{version}-py3-none-any.whl

Summary:        Extensions to the standard Python datetime module
Name:           python3-setuptools
# if you make any security fix in this package, package the whl files
# python3.spec without miss
Version:        65.5.1
Release:        5%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/setuptools

Source0: https://files.pythonhosted.org/packages/5f/36/7374297692bb9dbd7569a0f84887c7e5e314c41d5d9518cb76fbb130620d/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=e75eb7fdb0bc5ffdc76ed864cf753c2672d097a60f8747ac5cd40a49276d33df31fb619877234b4c22693b627d9978ecdd48a5c6c48aa0bbb856d48dec70fb0a

Patch0: CVE-2024-6345.patch

BuildRequires: python3-devel
BuildRequires: python3-xml

%define ExtraBuildRequires: python3-wheel

Requires:       python3
Requires:       python3-xml

BuildArch:      noarch

Provides:       python%{python3_version}dist(setuptools)

%description
Setuptools is a fully-featured, actively-maintained, and stable library
designed to facilitate packaging Python projects.
It helps developers to easily share reusable code (in the form of a library) and programs
(e.g., CLI/GUI tools implemented in Python), that can be installed with pip and uploaded to PyPI.

%package wheel
Summary:        The setuptools wheel

%description wheel
A Python wheel of setuptools to use with venv.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{python3} setup.py bdist_wheel

%install
%{py3_install}
find %{buildroot}%{python3_sitelib} -name '*.exe' | xargs rm -f
mkdir -p %{buildroot}%{python_wheel_dir}
install -p dist/%{python_wheel_name} -t %{buildroot}%{python_wheel_dir}

%check
%{py3_test}

%post
find %{python3_sitelib}/%{srcname}-* -type d -empty -delete

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,755)
%{python3_sitelib}/*

%files wheel
%defattr(-,root,root,755)
%dir %{python_wheel_dir}
%{python_wheel_dir}/%{python_wheel_name}

%changelog
* Tue Jul 23 2024 Prashant S Chauhan <prashant.singhj-chauhan@broadcom.com> 65.5.1-5
- Fix CVE-2024-6345
* Thu May 02 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 65.5.1-4
- Remove leftover empty setuptools dirs from install location
* Wed Mar 06 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 65.5.1-3
- Remove wheel dependency
* Tue Feb 20 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 65.5.1-2
- Add wheel files
* Tue Feb 07 2023 Prashant S Chauhan <psinghchauha@vmware.com> 65.5.1-1
- Separate python3-setuptools from python3.
