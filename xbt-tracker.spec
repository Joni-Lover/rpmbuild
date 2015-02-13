#
# spec file for package xbt-tracker WG
#
%define pkg_name xbtt
%define pkg_user xbt
%define pkg_homedir /var/lib/%{pkg_name}
%define pkg_rundir  /var/run/%{pkg_name}
%define pkg_logdir  /var/log/%{pkg_name}

# norootforbuild

Name:           xbt_tracker
Version:        0.2.8
Release:        437856.0%{?dist}
#
License:        GPLv2
Group:          Productivity/Networking/Other
#
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  boost141-devel cmake gcc-c++
BuildRequires:  mysql-devel >= 4.1
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires:    	initscripts >= 8.36
Requires(postun):   initscripts
# svn co $Url ; tar --exclude=XBT.props --exclude=.svn -z -c -v -f xbt_tracker.tar.gz xbt_tracker/
Url:            http://svn.wargaming.net/svn/WOT/web/xbt_tracker/
Source:         %{name}.tar.gz
Source1:        xbt_tracker.init
Source2:	xbt_tracker.conf

Summary:        A BitTorrent tracker written in C++

%description
XBT Tracker is a BitTorrent tracker written in C++. It's designed to offer high
performance while consuming little resources (CPU and RAM). It's a pure
tracker, so it doesn't offer a frontend.


Authors:
--------
    Olaf van der Spek
    modified by Wargaming.Net 

#%debug_package
%prep
%setup -q -n xbt_tracker
find -type d -name .svn -print0 | xargs -r0 rm -rfv

%build
export CFLAGS="%{optflags}   -Wall"
export CXXFLAGS="%{optflags} -Wall"
%if 0%{?suse_version} > 1000
    export CFLAGS="$CFLAGS -fstack-protector"
    export CXXFLAGS="$CXXFLAGS -fstack-protector"
%endif
cd ./Tracker
./make.sh -D_WG_EXT -D_WG_EXT_UPLOAD 
#-D_WG_TEST

%install
%{__install} -d -m 0755 %{buildroot}%{pkg_homedir} \
                        %{buildroot}%{pkg_rundir}  \
                        %{buildroot}%{pkg_logdir}

%{__install} -D -m 0755 Tracker/xbt_tracker %{buildroot}%{_sbindir}/xbt_tracker
%{__install} -D -m 0660 %{S:2} %{buildroot}%{_sysconfdir}/xbt_tracker.conf
%{__install} -D -m 0755 %{S:1} %{buildroot}%{_sysconfdir}/init.d/xbt_tracker

%clean
%{__rm} -rf %{buildroot}

%pre
/usr/sbin/groupadd -r %{pkg_user} &> /dev/null ||:
/usr/sbin/useradd  -g %{pkg_user} -s /bin/false -r -c "xbt tracker"  -d %{pkg_homedir} %{pkg_user} &> /dev/null ||:

%preun
/sbin/service %name stop >/dev/null 2>&1
/sbin/chkconfig --del %name
if [ -x /sbin/insserv ];then
	/sbin/insserv -r %{_sysconfdir}/init.d/%name
fi

%post
/sbin/chkconfig --add %name
if [ -x /sbin/insserv ];then
	/sbin/insserv %{_sysconfdir}/init.d/%name
fi

# Install mysql database manual
echo
echo 'Notes for install database for xbt tracker'
echo '=========================================='
echo
echo 'For start xbt tracker you need to create mysql database in you mysql-server'
echo 'SAMPLE: mysql -e "create database xbtt CHARACTER SET utf8;"'
echo
echo 'and create mysql user xbtt with password xbtt'
echo 'SAMPLE: mysql -e "GRANT all PRIVILEGES ON xbtt.* TO xbtt@'localhost' IDENTIFIED BY 'xbtt';"'
echo
echo 'after you need to install in new database dump file from /usr/share/doc/'%{name}'-'%{version}'/xbt_tracker.sql'
echo 'SAMPLE: mysql xbtt < /usr/share/doc/'%{name}'-'%{version}'/xbt_tracker.sql'
echo
echo '=========================================='

%files
%defattr(-,root,root,-)
%{_sbindir}/xbt_tracker
#
%doc Tracker/xbt_tracker.sql
%doc Tracker/xbt_tracker.conf.default
%doc README.txt
#
%dir %attr(750,%{pkg_user},%{pkg_user}) %{pkg_homedir}
%dir %attr(750,%{pkg_user},%{pkg_user}) %{pkg_rundir}
%dir %attr(750,%{pkg_user},%{pkg_user}) %{pkg_logdir}
#
%config(noreplace) %attr(660,root,%{pkg_user}) %{_sysconfdir}/xbt_tracker.conf
%config %{_sysconfdir}/init.d/xbt_tracker

%changelog
* Thu Jun 26 2014 Ivan Polonevich <joni @ wargaming dot net> - 0.2.8-437856.0
- Upstream release

* Wed Oct 16 2013 Ivan Polonevich <joni @ wargaming dot net> - 0.2.8-280765.7
- Delet D_WG_Test option from make

* Thu Jun 20 2013 Ivan Polonevich <joni @ wargaming dot net> - 0.2.8-280764.7
- Fix init script

* Mon Jun 17 2013 Ivan Polonevich <joni @ wargaming dot net> - 0.2.8-280764.5
- Change user to xbt

* Mon Jun 17 2013 Ivan Polonevich <joni @ wargaming dot net> - 0.2.8-280764.2
- Initial release


