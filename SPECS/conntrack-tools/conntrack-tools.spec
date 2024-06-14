Summary:        Connection tracking userspace tools for Linux.
Name:           conntrack-tools
Version:        1.4.6
Release:        4%{?dist}
License:        GPLv2
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://conntrack-tools.netfilter.org/
Source0:        http://netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha512  conntrack-tools=a48260308a12b11b584fcf4658ec2c4c1adb2801c9cf9a73fc259e5c30d2fbe401aca21e931972413f03e415f98fbf9bd678d2126faa6c6d5748e8a652e58f1a
Source1:        conntrackd.conf
Source2:        conntrackd.service

BuildRequires: gcc
BuildRequires: systemd-devel
BuildRequires: libtirpc-devel
BuildRequires: libmnl-devel
BuildRequires: libnfnetlink-devel
BuildRequires: libnetfilter_conntrack-devel
BuildRequires: libnetfilter_cttimeout-devel
BuildRequires: libnetfilter_cthelper-devel
BuildRequires: libnetfilter_queue-devel
BuildRequires: bison
BuildRequires: flex
BuildRequires: systemd

Requires:      systemd
Requires:      libmnl
Requires:      libnetfilter_conntrack
Requires:      libnetfilter_cthelper
Requires:      libnetfilter_cttimeout
Requires:      libnetfilter_queue
Requires:      libnfnetlink
Provides:      conntrack

%description
The conntrack-tools are a set of free software userspace tools for Linux that
allow system administrators interact with the Connection Tracking System,
which is the module that provides stateful packet inspection for iptables.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure --disable-static --enable-systemd
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
mkdir -p %{buildroot}%{_sysconfdir}/conntrackd
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/conntrackd/
install -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/

%files
%dir %{_sysconfdir}/conntrackd
%config(noreplace) %{_sysconfdir}/conntrackd/conntrackd.conf
%{_unitdir}/conntrackd.service
%{_sbindir}/conntrack
%{_sbindir}/conntrackd
%{_sbindir}/nfct
%dir %{_libdir}/conntrack-tools
%{_libdir}/conntrack-tools/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%post
%systemd_post conntrackd.service

%preun
%systemd_preun conntrackd.service

%postun
%systemd_postun conntrackd.service

%changelog
*  Fri Jun 14 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.6-4
-  Fix conntrackd.service failure
*  Sun Oct 17 2021 Susant Sahani <ssahani@vmware.com.com> 1.4.6-3
-  Rename conntrackd.conf eth2 -> eth0
*  Sat Feb 27 2021 Andrew Williams <andy@tensixtyone.com> 1.4.6-2
-  Add provide for conntrack
*  Tue Aug 25 2020 Ashwin H <ashwinh@vmware.com> 1.4.6-1
-  Initial version
