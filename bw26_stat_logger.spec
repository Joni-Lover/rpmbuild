Name:           bw26_stat_logger
Version:        1.7
Release:        2%{?dist}
Summary:        stat_logger for bigworld 2.6

Group:          Middleware/MMOG
License:        BigWorld License
URL:            https://jira.wargaming.net/browse/WGSA-7485
Source0:        https://svn.wargaming.net/svn/WOT/deployment/bw26_stat_logger/%{name}-%{version}.tar.gz
#curl -u "user:pass" "https://svn.wargaming.net/svn/WOT/deployment/bw26_stat_logger/bw26_stat_logger-1.3.tar.gz" -o bw26_stat_logger-1.3.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This package contains the BW stat_logger component of the BigWorld Server.

%prep
%setup -q  -c %{name}-%{version}

%post 
chown -R bwtools:bwtools /opt/bigworld/2.6dev/ /etc/bigworld/stat_logger.xml.example

for dir in /var/log/bigworld /var/run/bigworld; do
	if ! test -d $dir; then
		mkdir -p $dir
	fi
	chown -R "bwtools:bwtools" $dir
done
 

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %{buildroot}
cp -ar * %{buildroot}/ 

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/etc/bigworld/stat_logger.xml.example
/opt/*

%changelog
* Mon Sep 08 2014 Anton Samets <a_samets@wargaming.net> - 1.7-2
- new version

* Thu Aug 21 2014 Anton Samets <a_samets@wargaming.net> - 1.7-1
- New upstream release

* Tue Jun 17 2014 Ivan Polonevich <joni @ wargaming dot net> - 1.5-1
- Update upstream

* Fri Jun 13 2014 Ivan Polonevich <joni @ wargaming dot net> - 1.4-1
- Update upstream

* Mon Jun 09 2014 Ivan Polonevich <joni @ wargaming dot net> - 1.3-1
- Update upstream

* Mon Mar 31 2014 Ivan Polonevich <joni @ wargaming dot net> - 1.2-1
- Update upstream

* Tue Feb 25 2014 Ivan Polonevich <joni @ wargaming dot net> - 1.0-1
- Initial rpm

