%{?_javapackages_macros:%_javapackages_macros}
# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define originalname PullParser

Summary:        XML Pull Parser
Name:           xpp2
Version:        2.1.10
Release:        18.1%{?dist}
Epoch:          0
License:        xpp and ASL 1.1 and Public Domain
URL:            https://www.extreme.indiana.edu/xgws/xsoap/xpp/

Source0:        http://www.extreme.indiana.edu/xgws/xsoap/xpp/download/PullParser2/PullParser2.1.10.tgz
Patch0:         xpp2-build_xml.patch
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  junit
BuildRequires:  xml-commons-apis
Requires:       xml-commons-apis
Requires:       jpackage-utils
BuildArch:      noarch
Provides:  xpp2-doc = 0:%{version}-%{release}
Obsoletes: xpp2-doc < 0:2.1.10-18

%description
XML Pull Parser 2 (XPP2) is a simple and fast incremental XML parser.
NOTE: XPP2 is no longer developed and is on maintenance mode.
All active development concentrates on its successor XPP3/MXP1.

%package javadoc
Summary:        Javadoc for %{name}


%description javadoc
%{summary}.

%package demo
Summary:        Samples for %{name}

Requires:       %{name} = %{epoch}:%{version}

%description demo
%{summary}.

%prep
%setup -q -n %{originalname}%{version}
# remove all binary libs and prebuilt classes
find \( -name *.class -o -name *.jar \) -delete

%patch0 -b .sav

# Fix encoding of licence file
iconv -f ISO-8859-1 -t UTF-8 LICENSE.txt > LICENSE.txt.utf8
mv LICENSE.txt.utf8 LICENSE.txt

%build
export CLASSPATH=$(build-classpath xml-commons-apis)
ant all api api.impl
CLASSPATH=$CLASSPATH:$(build-classpath junit):build/tests:build/lib/PullParser-2.1.10.jar
java AllTests

%install
# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}

cp -p build/lib/%{originalname}-intf-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-intf.jar
cp -p build/lib/%{originalname}-standard-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-standard.jar
cp -p build/lib/%{originalname}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
cp -p build/lib/%{originalname}-x2-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-x2.jar

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}/api
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}/api_impl
cp -pr doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}/api
cp -pr doc/api_impl/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}/api_impl
rm -rf doc/{build.txt,api,api_impl}

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr src/java/samples/* $RPM_BUILD_ROOT%{_datadir}/%{name}

%pretrans javadoc
# workaround for rpm bug, can be removed in F-23
[ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%pretrans demo
# workaround for rpm bug, can be removed in F-23
[ -L %{_datadir}/%{name} ] && \
rm -rf $(readlink -f %{_datadir}/%{name}) %{_datadir}/%{name} || :

%files
%doc LICENSE.txt README.html doc
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-intf.jar
%{_javadir}/%{name}-standard.jar
%{_javadir}/%{name}-x2.jar

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/%{name}

%files demo
%{_datadir}/%{name}

%changelog
* Mon Aug 26 2013 Mat Booth <fedora@matbooth.co.uk> - 0:2.1.10-18
- Update for newer guidelines, drop versioned jars, duplicate docs
- Fixes rhbz #993885, rhbz #1001270

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.1.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.1.10-16
- Remove prebuilt classes
- Resolves: rhbz#959429

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.1.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 15 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.1.10-14
- The license is actually a mixture of ASL 1.1, xpp and Public Domain

* Wed Aug 15 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.1.10-13
- Fix license from ASL to xpp (new license type)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.1.10-11.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.1.10-10.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.1.10-9.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar 10 2010 Peter Lemenkov <lemenkov@gmail.com> - 0:2.1.10-8.3
- Added missing requires - jpackage-utils

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.1.10-8.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.1.10-7.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.1.10-6.2
- drop repotag
- fix license tag

* Tue Feb 13 2007 Permaine Cheung <pcheung@redhat.com> - 0:2.1.10-6jpp.1
- Fix release, license, buildroot, typo, and other rpmlint issues.
- Got rid of Vendor and Distribution.
- Rename manual subpackage to doc.
- Move README and LICENSE file back into main package, and mark all docs.

* Tue Apr 11 2006 Ralph Apel <r.apel at r-apel.de> - 0:2.1.10-6jpp
- First JPP-1.7 release

* Wed Aug 10 2005 Ralph Apel <r.apel at r-apel.de> - 0:2.1.10-5jpp
- Fix Bug 17 installed but unpackaged symlinks
- Patch build.xml for source=1.4 and target=1.4

* Thu Aug 26 2004 Ralph Apel <r.apel at r-apel.de> - 0:2.1.10-4jpp
- Build with ant-1.6.2
- Relax some versioned dependencies

* Tue Jun 01 2004 Randy Watler <rwatler at finali.com> - 0:2.1.10-3jpp
- Upgrade to Ant 1.6.X

* Mon Jan 19 2004 Ralph Apel <r.apel@r-apel.de> - 0:2.1.10-2jpp
- Fix rpm var _originalname to originalname
- Include versionless symlinks for javadoc, manual and demo
- demo requires main package

* Thu Jan 15 2004 Ralph Apel <r.apel@r-apel.de> - 0:2.1.10-1jpp
- First JPackage build
