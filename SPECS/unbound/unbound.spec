Summary:        unbound dns server
Name:           unbound
Version:        1.13.1
Release:        1%{?dist}
Group:          System/Servers
Vendor:         VMware, Inc.
License:        BSD
Distribution:   Photon
URL:            http://www.unbound.net
Source0:        https://www.unbound.net/downloads/%{name}-%{version}.tar.gz
%define sha1    unbound=561522b06943f6d1c33bd78132db1f7020fc4fd1
Source1:        %{name}.service
Requires:       systemd
BuildRequires:  systemd
BuildRequires:  expat
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd

%description
Unbound is a validating, recursive, and caching DNS resolver.

%package	devel
Summary:	unbound development libs and headers
Group:		Development/Libraries
%description devel
Development files for unbound dns server

%package	docs
Summary:	unbound docs
Group:		Documentation
%description docs
unbound dns server docs

%prep
%setup -q

%build
%configure \
    --with-conf-file=%{_sysconfdir}/%{name}/unbound.conf \
    --disable-static
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
find %{buildroot} -name '*.la' -delete
install -vdm755 %{buildroot}%{_unitdir}
install -pm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%check
make check

%pre
getent group unbound >/dev/null || groupadd -r unbound
getent passwd unbound >/dev/null || \
useradd -r -g unbound -d %{_sysconfdir}/unbound -s /sbin/nologin \
-c "Unbound DNS resolver" unbound

%post
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_sbindir}/*
%config(noreplace) %{_sysconfdir}/unbound/unbound.conf
%{_unitdir}/%{name}.service

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files docs
%{_mandir}/*

%changelog
*  Tue Feb 15 2022 Nitesh Kumar <kunitesh@vmware.com> 1.13.1-1
-  Upgrade to 1.13.1 to fix bunch of CVE's
*  Wed May 05 2021 Shreyas B. <shryasb@vmware.com> 1.6.8-4
-  Fix for CVE-2019-25031
-  Fix for CVE-2019-25034
-  Fix for CVE-2019-25035
-  Fix for CVE-2019-25036
-  Fix for CVE-2019-25037
-  Fix for CVE-2019-25042
*  Tue Feb 02 2021 Shreyas B. <shryasb@vmware.com> 1.6.8-3
-  Fix for CVE-2020-28935
*  Sun May 24 2020 Shreyas B. <shryasb@vmware.com> 1.6.8-2
-  Fix for CVE-2020-12662 & CVE-2020-12663
*  Mon Feb 3 2020 Michelle Wang <michellew@vmware.com> 1.6.8-1
-  CVE-2017-15105: bump up version since 1.6.8 is released with the patch
*  Fri Oct 6 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-3
-  update service file for restart and pid.
*  Tue Sep 26 2017 Anish Swaminathan <anishs@vmware.com> 1.6.0-2
-  Release bump for expat version update
*  Fri Jan 06 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-1
-  Initial
