# TODO
# - -demos package

%define		_rc	2

%include	/usr/lib/rpm/macros.java
Summary:	Red5: Open Source Flash Server
Summary(pl.UTF-8):	Red5: Otwarty serwer Flasha
Name:		red5
Version:	0.9
Release:	0.%{_rc}.1
License:	LGPL
Group:		Networking/Daemons/Java
# wget -c http://www.red5.org/downloads/0_9/red5-0.9.RC2.tar.gz
Source0:	red5-0.9.RC2.tar.gz
# Source0-md5:	b1150391591f4ea6cdc30b38fd3732eb
NoSource:	0
Source1:	%{name}
Source2:	%{name}.init
Source3:	%{name}.sysconfig
URL:		http://red5.org/
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	eclipse-jdt
Requires:	rc-scripts
Requires:	java-tomcat-catalina >= 6.0.20-7
Requires:	java-tomcat-coyote >= 6.0.20-7
Requires:	java-tomcat-jasper >= 6.0.20-7
Suggests:	tomcat-native
Provides:	group(red5)
Provides:	group(servlet)
Provides:	user(red5)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appconfdir	%{_sysconfdir}/%{name}
%define		_appdatadir	%{_datadir}/%{name}
%define		_appstatedir	%{_localstatedir}/lib/%{name}
%define		_applogdir	%{_var}/log/%{name}

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

%prep
%setup -q -c

rm lib/catalina-*.jar
rm lib/jasper-*.jar
rm lib/tomcat-coyote-*.jar

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdatadir},%{_sbindir},%{_appstatedir}/work,%{_appconfdir},%{_applogdir}}
install -d $RPM_BUILD_ROOT{/etc/sysconfig,/etc/rc.d/init.d,/var/run/red5}

cp -a {red5.jar,boot.jar,lib} $RPM_BUILD_ROOT%{_appdatadir}
cp -a webapps $RPM_BUILD_ROOT%{_appstatedir}
cp -a conf/* $RPM_BUILD_ROOT%{_appconfdir}

ln -s %{_appconfdir} $RPM_BUILD_ROOT%{_appdatadir}/conf
ln -s %{_appstatedir}/webapps $RPM_BUILD_ROOT%{_appdatadir}/webapps
ln -s %{_appstatedir}/work $RPM_BUILD_ROOT%{_appdatadir}/work
ln -s %{_applogdir} $RPM_BUILD_ROOT%{_appdatadir}/log

install %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/red5
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/red5

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 237 -r -f servlet
%groupadd -g 243 -r -f red5
%useradd -u 243 -r -d /var/lib/red5 -s /bin/false -c "red5 user" -g red5 -G servlet red5

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

%files
%defattr(644,root,root,755)
%doc license.txt
%{_appdatadir}
%dir %attr(775,red5,red5) %{_appstatedir}
%attr(775,red5,red5) %{_appstatedir}/work
%attr(775,red5,servlet) %{_appstatedir}/webapps
%attr(775,red5,red5) %{_applogdir}
%dir %{_appconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_appconfdir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(770,root,red5) /var/run/%{name}
%attr(755,root,root) %{_sbindir}/%{name}
