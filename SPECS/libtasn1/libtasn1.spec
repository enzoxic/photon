Summary:        ASN.1 library
Name:           libtasn1
Version:        4.14
Release:        2%{?dist}
License:        GPLv3+ and LGPLv2+
URL:            http://www.gnu.org/software/libtasn1/
Source0:        http://ftp.gnu.org/gnu/libtasn1/%{name}-%{version}.tar.gz
%define sha1    %{name}=4ce6a70a40f50a2c29a62bbf1c0c5b6e306ca4e3
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Patch0:         libtasn1-CVE-2021-46848.patch

%description
Libtasn1 library provides Abstract Syntax Notation One (ASN.1, as specified by
the X.680 ITU-T recommendation) parsing and structures management, and
Distinguished Encoding Rules (DER, as per X.690) encoding and decoding
functions.

%package devel
Summary:    Development libraries and header files for libtasn1
Requires:   %{name} = %{version}-%{release}
Provides:   pkgconfig(libtasn1)

%description devel
The package contains libraries and header files for
developing applications that use libtasn1.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
rm %{buildroot}%{_infodir}/*
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_mandir}/man3/*

%changelog
*   Tue Oct 25 2022 Ankit Jain <ankitja@vmware.com> 4.14-2
-   Fixes CVE-2021-46848
*   Mon Apr 13 2020 Siddharth Chandrasekran <csiddhath@vmware.com> 4.14-1
-   Update to version 4.14 to fix CVE-2018-1000654
*   Mon Feb 12 2018 Xiaolin Li <xiaolinl@vmware.com> 4.13-1
-   Update to version 4.13 fix CVE-2018-6003.
*   Tue Oct 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.12-1
-   update to 4.12 and apply patch for CVE-2017-10790
*   Tue Apr 04 2017 Kumar Kaushik <kaushikk@vmware.com> 4.10-1
-   Upgrading version to 4.10
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 4.7-4
-   Moved man3 to devel subpackage.
*   Wed Nov 30 2016 Dheeraj Shetty <dheerajs@vmware.com> 4.7-3
-   Added patch for CVE-2016-4008
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.7-2
-   GA - Bump release of all rpms
*   Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 4.7-1
-   Updated to version 4.7
*   Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 4.5-3
-   Moving static lib files to devel package.
*   Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 4.5-2
-   Removing la files from packages.
*   Fri Jun 19 2015 Divya Thaluru <dthaluru@vmware.com> 4.5-1
-   Initial build. First version
