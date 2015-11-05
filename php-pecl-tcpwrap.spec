#
# Conditional build:
%bcond_without	tests		# build without tests

%define		php_name	php%{?php_suffix}
%define		modname	tcpwrap
%define		status		stable
Summary:	%{modname} - tcpwrapper bindings
Summary(pl.UTF-8):	%{modname} - dowiązania tcpwrapper
Name:		%{php_name}-pecl-%{modname}
Version:	1.1.3
Release:	10
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	6db26ebbf6c59fedf2228e662fe78e3e
Patch0:		branch.diff
URL:		http://pecl.php.net/package/tcpwrap/
BuildRequires:	%{php_name}-devel >= 3:5.0.4
BuildRequires:	libwrap-devel
BuildRequires:	rpmbuild(macros) >= 1.650
%{?with_tests:BuildRequires:	%{php_name}-cli}
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-tcpwrap < 1.1.3-7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package handles /etc/hosts.allow and /etc/hosts.deny files.

In PECL status of this package is: %{status}.

%description -l pl.UTF-8
Za pomocą tego pakietu możliwa jest obsługa plików /etc/hosts.allow
oraz /etc/hosts.deny.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .
%patch0 -p0

%build
phpize
%configure
%{__make}

%if %{with tests}
# simple module load test
%{__php} -n \
	-dextension_dir=modules \
	-dextension=%{modname}.so \
	-m > modules.log
grep %{modname} modules.log
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}
install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
