# TODO
# - packaging
#
%define		_rc		rc2
%define		_rel	0.1
Summary:	Red5: Open Source Flash Server
Summary(pl.UTF-8):	Red5: Otwarty serwer Flasha
Name:		red5
Version:	0.6
Release:	0.%{_rc}.%{_rel}
License:	LGPL
Group:		Applications
Source0:	http://dl.fancycode.com/red5/%{name}-%{version}%{_rc}.tar.gz
# Source0-md5:	7c41ff734cd8153cb3ec37104f5954c1
URL:		http://www.osflash.org/red5/
BuildRequires:	ant
BuildRequires:	jaxp_parser_impl
BuildRequires:	jdk >= 1.6
BuildRequires:	rpmbuild(macros) >= 1.300
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Red5 is an Open Source Flash Server written in Java that supports:
- Streaming Audio/Video (FLV and MP3)
- Recording Client Streams (FLV only)
- Shared Objects
- Live Stream Publishing
- Remoting

%description -l pl.UTF-8
Red5 to napisany w Javie otwarty serwer Flasha obsługujący:
- Strumieniowanie Audio/Wideo (FLV oraz MP3)
- Nagrywanie strumieni klienta (tylko FLV)
- Współdzielenie obiektów
- Publikowanie strumieni na żywo

%package javadoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{name} -

%description javadoc -l pl.UTF-8
Dokumentacja do %{name} -

%prep
%setup -q -n %{name}-%{version}%{_rc}

%build
# some source files contain '»' character and javac barfs on that
export LC_ALL=en_US
%ant dist

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# install jar
cp -a dist/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a dist/doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
