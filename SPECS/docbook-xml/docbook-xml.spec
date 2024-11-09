Summary:        Docbook-xml-4.5
Name:           docbook-xml
Version:        4.5
Release:        12%{?dist}
URL:            http://www.docbook.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://www.docbook.org/xml/4.5/%{name}-%{version}.zip
%define sha512  %{name}=1ee282fe86c9282610ee72c0e1d1acfc03f1afb9dc67166f438f2703109046479edb6329313ecb2949db27993077e077d111501c10b8769ebb20719eb6213d27

Source1: license.txt
%include %{SOURCE1}

Requires:       libxml2

BuildRequires:  libxml2
BuildRequires:  unzip

BuildArch:      noarch

%description
The DocBook XML DTD-4.5 package contains document type definitions for
verification of XML data files against the DocBook rule set. These are
useful for structuring books and software documentation to a standard
allowing you to utilize transformations already written for that standard.
%prep
%autosetup -c -T -p1
unzip %{SOURCE0}
if [ `id -u` -eq 0 ]; then
  chown -R root.root .
  chmod -R a+rX,g-w,o-w .
fi
%build
%install
install -v -d -m755 %{buildroot}/usr/share/xml/docbook/%{name}-%{version}
install -v -d -m755 %{buildroot}/etc/xml
chown -R root:root .
cp -v -af docbook.cat *.dtd ent/ *.mod %{buildroot}/usr/share/xml/docbook/%{name}-%{version}

%post
if [ ! -e /etc/xml/docbook ]; then
    xmlcatalog --noout --create /etc/xml/docbook
fi &&
xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML V4.5//EN" \
    "http://www.oasis-open.org/docbook/xml/4.5/docbookx.dtd" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML CALS Table Model V4.5//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/calstblx.dtd" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//DTD XML Exchange Table Model 19990315//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/soextblx.dtd" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Information Pool V4.5//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/dbpoolx.mod" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML Document Hierarchy V4.5//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/dbhierx.mod" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//ELEMENTS DocBook XML HTML Tables V4.5//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/htmltblx.mod" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Notations V4.5//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/dbnotnx.mod" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Character Entities V4.5//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/dbcentx.mod" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "public" \
    "-//OASIS//ENTITIES DocBook XML Additional General Entities V4.5//EN" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5/dbgenent.mod" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "rewriteSystem" \
    "http://www.oasis-open.org/docbook/xml/4.5" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5" \
    /etc/xml/docbook &&
xmlcatalog --noout --add "rewriteURI" \
    "http://www.oasis-open.org/docbook/xml/4.5" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5" \
    /etc/xml/docbook

if [ ! -e /etc/xml/catalog ]; then
    xmlcatalog --noout --create /etc/xml/catalog
fi &&
xmlcatalog --noout --add "delegatePublic" \
    "-//OASIS//ENTITIES DocBook XML" \
    "file:///etc/xml/docbook" \
    /etc/xml/catalog &&
xmlcatalog --noout --add "delegatePublic" \
    "-//OASIS//DTD DocBook XML" \
    "file:///etc/xml/docbook" \
    /etc/xml/catalog &&
xmlcatalog --noout --add "delegateSystem" \
    "http://www.oasis-open.org/docbook/" \
    "file:///etc/xml/docbook" \
    /etc/xml/catalog &&
xmlcatalog --noout --add "delegateURI" \
    "http://www.oasis-open.org/docbook/" \
    "file:///etc/xml/docbook" \
    /etc/xml/catalog

for DTDVERSION in 4.1.2 4.2 4.3 4.4
do
  xmlcatalog --noout --add "public" \
    "-//OASIS//DTD DocBook XML V$DTDVERSION//EN" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION/docbookx.dtd" \
    /etc/xml/docbook
  xmlcatalog --noout --add "rewriteSystem" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5" \
    /etc/xml/docbook
  xmlcatalog --noout --add "rewriteURI" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION" \
    "file:///usr/share/xml/docbook/docbook-xml-4.5" \
    /etc/xml/docbook
  xmlcatalog --noout --add "delegateSystem" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION/" \
    "file:///etc/xml/docbook" \
    /etc/xml/catalog
  xmlcatalog --noout --add "delegateURI" \
    "http://www.oasis-open.org/docbook/xml/$DTDVERSION/" \
    "file:///etc/xml/docbook" \
    /etc/xml/catalog
done

%preun
if [ $1 -eq 0 ] ; then
    if [ -f /etc/xml/catalog ]; then
        xmlcatalog --noout --del \
        "file:///etc/xml/docbook" /etc/xml/catalog
    fi
    if [ -f /etc/xml/docbook ]; then
        xmlcatalog --noout --del \
        "file:///usr/share/xml/docbook/docbook-xml-4.5" /etc/xml/docbook

        for DTDVERSION in 4.1.2 4.2 4.3 4.4 %{version}
        do
            xmlcatalog --noout --del \
            "http://www.oasis-open.org/docbook/xml/$DTDVERSION/docbookx.dtd" /etc/xml/docbook
        done

        for file in `find /usr/share/xml/docbook/%{name}-%{version}/*.dtd -printf "%f\n"`
        do
            xmlcatalog --noout --del \
            "file:///usr/share/xml/docbook/docbook-xml-4.5/$file" /etc/xml/docbook
        done

        for file in `find /usr/share/xml/docbook/%{name}-%{version}/*.mod -printf "%f\n"`
        do
            xmlcatalog --noout --del \
            "file:///usr/share/xml/docbook/docbook-xml-4.5/$file" /etc/xml/docbook
        done
    fi
fi

%files
%defattr(-,root,root)
/usr/share/xml/docbook/%{name}-%{version}
/etc/xml

%changelog
*   Tue Nov 12 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 4.5-12
-   Update license field
*   Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.5-11
-   Release bump for SRP compliance
*   Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.5-10
-   Bump version as a part of libxml2 upgrade
*   Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 4.5-9
-   Release bump up to use libxml2 2.9.12-1.
*   Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 4.5-8
-   Remove libxml2-python from requires.
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.5-7
-   Fix arch
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.5-6
-   GA - Bump release of all rpms
*   Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  4.5-5
-   Fixing spec file to handle rpm upgrade scenario correctly
*   Thu Mar 10 2016 XIaolin Li <xiaolinl@vmware.com> 4.5.1-4
-   Correct the local folder name.
*   Mon Jul 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.5.1-3
-   Updated dependencies.
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 4.5.1-2
-   Updated group.
*   Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 4.5-1
-   Initial build. First version
