%define		_modname	tcpwrap
%define		_status		stable
Summary:	%{_modname} - tcpwrapper bindings
Summary(pl):	%{_modname} - dowi±zania tcpwrapper
Name:		php-pecl-%{_modname}
Version:	1.0
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	ed68d289c6ce0155b2bd6e62b6ed0996
URL:		http://pecl.php.net/package/tcpwrap/
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	php-devel
Requires:	php-common
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
This package handles /etc/hosts.allow and /etc/hosts.deny files.

In PECL status of this package is: %{_status}.

%description -l pl
Za pomoc± tego pakietu mo¿liwa jest obs³uga plików /etc/hosts.allow
oraz /etc/hosts.deny.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php-cgi.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php-cgi.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,EXPERIMENTAL}
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
