# TODO
# - packaging
# - -demos package
#
Summary:	Red5: Open Source Flash Server
Summary(pl.UTF-8):	Red5: Otwarty serwer Flasha
Name:		red5
Version:	0.8.0
Release:	0.1
License:	LGPL
Group:		Applications
Source0:	http://www.red5.org/downloads/0_8/red5-0.8.0.tar.gz
# Source0-md5:	7be9296e6369a52b3607cfce1ac7ee01
Source1:	%{name}
URL:		http://red5.org/
BuildRequires:	rpmbuild(macros) >= 1.300
Provides:       group(servlet)
Provides:       user(red5)
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
%setup -c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_localstatedir}/%{name}}

cp -a {conf,lib,webapps} $RPM_BUILD_ROOT%{_appdir}
cp -a red5.jar $RPM_BUILD_ROOT%{_appdir}

mv $RPM_BUILD_ROOT%{_appdir}/webapps $RPM_BUILD_ROOT%{_localstatedir}/%{name}/webapps

install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/red5

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 237 -r -f servlet
%useradd -u 243 -r -d /var/lib/red5 -s /bin/false -c "red5 user" -g servlet red5

%post
/sbin/chkconfig --add red5
%service red5 restart

%preun
if [ "$1" = "0" ]; then
	%service red5 stop
	/sbin/chkconfig --del red5
fi

%postun
if [ "$1" = "0" ]; then
	%userremove red5
	%groupremove servlet
fi

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc license.txt
%attr(755,root,root) %{_bindir}/red5
%{_appdir}
%attr(775,red5,servlet) %{_localstatedir}/%{name}

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
