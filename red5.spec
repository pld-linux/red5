# TODO
# - -demos package
# - use more jar libraries from javadir instead of bundled ones
#
# Conditional build:
%bcond_with	javadoc		# don't build javadoc

Summary:	Red5: Open Source Flash Server
Summary(pl.UTF-8):	Red5: Otwarty serwer Flasha
Name:		red5
Version:	1.0.1
Release:	0.1
License:	Apache v2.0
Group:		Networking/Daemons/Java
Source0:	http://www.red5.org/downloads/red5/1_0_1/%{name}-%{version}.tar.gz
# Source0-md5:	874fb6428907e47d107f204dfab5775a
Source1:	%{name}
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source4:	%{name}.tmpfiles
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
Requires:	java-eclipse-jdt
Requires:	java-tomcat-catalina >= 6.0.20-7
Requires:	java-tomcat-coyote >= 6.0.20-7
Requires:	java-tomcat-jasper >= 6.0.20-7
Requires:	rc-scripts
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

%package javadoc
Summary:	Online manual for %{name}
Summary(pl.UTF-8):	Dokumentacja online do %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
API documentation for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja API do %{name}.

%prep
%setup -q -n %{name}-server-1.0

rm plugins/catalina-*.jar
rm plugins/jasper-*.jar
rm plugins/tomcat-coyote-*.jar

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdatadir},%{_sbindir},%{_appstatedir}/work,%{_appconfdir},%{_applogdir}} \
	$RPM_BUILD_ROOT{/etc/sysconfig,/etc/rc.d/init.d,/var/run/red5} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

cp -a red5-*.jar lib $RPM_BUILD_ROOT%{_appdatadir}
cp -a webapps $RPM_BUILD_ROOT%{_appstatedir}
cp -a conf/* $RPM_BUILD_ROOT%{_appconfdir}

ln -s %{_appconfdir} $RPM_BUILD_ROOT%{_appdatadir}/conf
ln -s %{_appstatedir}/webapps $RPM_BUILD_ROOT%{_appdatadir}/webapps
ln -s %{_appstatedir}/work $RPM_BUILD_ROOT%{_appdatadir}/work
ln -s %{_applogdir} $RPM_BUILD_ROOT%{_appdatadir}/log

install -p %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/%{name}
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/red5
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/red5
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
%endif

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

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

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
%{systemdtmpfilesdir}/%{name}.conf
%attr(755,root,root) %{_sbindir}/%{name}

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif
