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

%define gcj_support  1
%define originalname PullParser

Summary:        XML Pull Parser
Name:           xpp2
Version:        2.1.10
Release:        %mkrel 6.1.4
Epoch:          0
License:        Apache Software License
URL:            http://www.extreme.indiana.edu/xgws/xsoap/xpp/
Group:          Development/Java
Source0:        http://www.extreme.indiana.edu/xgws/xsoap/xpp/download/PullParser2/PullParser2.1.10.tgz
Patch0:         xpp2-build_xml.patch
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  java-devel
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  junit
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-jaxp-1.3-apis
Requires:       xml-commons-jaxp-1.3-apis
Requires:       jpackage-utils
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
XML Pull Parser 2 (XPP2) is a simple and fast incremental XML parser.
NOTE: XPP2 is no longer developed and is on maintenance mode. 
All active development concentrates on its successor XPP3/MXP1.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}.

%package doc
Summary:        Manual for %{name}
Group:          Development/Java

%description doc
%{summary}.

%package demo
Summary:        Samples for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}

%description demo
%{summary}.

%prep
%setup -q -n %{originalname}%{version}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%patch0 -b .sav

%build
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=$(build-classpath xerces-j2 xml-commons-jaxp-1.3-apis)
%{ant} all api api.impl
CLASSPATH=$CLASSPATH:$(build-classpath junit):build/tests:build/lib/PullParser-2.1.10.jar
%{java} AllTests

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}

cp -p build/lib/%{originalname}-intf-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-intf-%{version}.jar
cp -p build/lib/%{originalname}-standard-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-standard-%{version}.jar
cp -p build/lib/%{originalname}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -p build/lib/%{originalname}-x2-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-x2-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/api
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/api_impl
cp -pr doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/api
cp -pr doc/api_impl/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/api_impl
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}


rm -rf doc/{build.txt,api,api_impl}

# doc
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
cp -pr doc/* $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/doc/%{name}

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr src/java/samples/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc README.html
%doc LICENSE.txt
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}-intf.jar
%{_javadir}/%{name}-intf-%{version}.jar
%{_javadir}/%{name}-standard.jar
%{_javadir}/%{name}-standard-%{version}.jar
%{_javadir}/%{name}-x2.jar
%{_javadir}/%{name}-x2-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files doc
%defattr(0644,root,root,0755)
%doc %{_datadir}/doc/%{name}-%{version}
%doc %{_datadir}/doc/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}-%{version}
%{_datadir}/%{name}
