Summary:        Library for the arithmetic of complex numbers
Name:           mpc
Version:        1.3.1
Release:        2%{?dist}
URL:            http://www.multiprecision.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.multiprecision.org/mpc/download/%{name}-%{version}.tar.gz
%define sha512 mpc=4bab4ef6076f8c5dfdc99d810b51108ced61ea2942ba0c1c932d624360a5473df20d32b300fc76f2ba4aa2a97e1f275c9fd494a1ba9f07c4cb2ad7ceaeb1ae97

Source1: license.txt
%include %{SOURCE1}

Requires:       gmp

%description
The MPC package contains a library for the arithmetic of complex
numbers with arbitrarily high precision and correct rounding of
the result.

%prep
%autosetup

%build
%configure \
      --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.so.*

%changelog
* Tue Sep 24 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.3.1-2
- Bump version to generate SRP provenance file
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.1-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.2.1-1
- Automatic Version Bump
* Wed Sep 04 2019 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-2
- Bump up release number to get generic mtune option from gmp.h
* Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.1.0-1
- Update to version 1.1.0
* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 1.0.3-3
- Modified check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.3-2
- GA - Bump release of all rpms
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  1.0.3-1
- Update version.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.0.2-1
- Initial build. First version
