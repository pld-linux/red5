# TODO
# - packaging
#
%define		_rc		rc2
%define		_rel	0.1
Summary:	Red5 : Open Source Flash Server
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

%prep
%setup -q -n %{name}-%{version}%{_rc}

%build
# some source files contain '»' character and javac barfs on that
export LC_ALL=en_US
%ant dist

%install
rm -rf $RPM_BUILD_ROOT
	DESTINATION=$RPM_BUILD_ROOT%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
