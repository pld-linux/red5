# TODO
# - packaging
#
Summary:	Red5: Open Source Flash Server
Summary(pl.UTF-8):	Red5: Otwarty serwer Flasha
Name:		red5
Version:	0.6.2
Release:	0.2
License:	LGPL
Group:		Applications
Source0:	http://dl.fancycode.com/red5/%{name}-%{version}.tar.gz
# Source0-md5:	ed769422e86359922433de3805a0e361
Source1:	%{name}
URL:		http://www.osflash.org/red5/
BuildRequires:	ant
BuildRequires:	jaxp_parser_impl
BuildRequires:	jdk >= 1.6
BuildRequires:	rpmbuild(macros) >= 1.300
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/%{name}

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
Documentation for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{name}.

%prep
%setup -q

%build
# some source files contain '»' character and javac barfs on that
export LC_ALL=en_US
%ant dist

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir}}

cp -a dist/* $RPM_BUILD_ROOT%{_appdir}
rm -rf $RPM_BUILD_ROOT%{_appdir}/doc
rm -f $RPM_BUILD_ROOT%{_appdir}/red5.{bat,sh}
install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/red5

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
%attr(755,root,root) %{_bindir}/red5
%{_appdir}

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
