%define libname %mklibname spreadsheet %version
%define develname %mklibname -d spreadsheet
%define goffice %(rpm -q --queryformat %%{VERSION} goffice)

Name: gnumeric
Summary: A full-featured spreadsheet for GNOME
Version: 1.9.0
Release: %mkrel 1
License: GPLv2+
Group: Office
Source0: http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Source2: %{name}-32.png
Source3: %{name}-16.png
Source4: %{name}-48.png
Patch: gnumeric-1.7.11-desktopfile.patch
# gw: hardcode help file path (bug #33798)
Patch1: gnumeric-1.7.12-help-path.patch
Patch3: gnumeric-1.8.0-missing.patch
URL:http://www.gnome.org/projects/gnumeric/
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

Requires: %libname = %version
BuildRequires:	libgnomeui2-devel
BuildRequires:  libgsf-devel >= 1:1.14.6
BuildRequires:  libgoffice-devel >= 0.6.3
BuildRequires:  libglade2.0-devel
BuildRequires:  libgnomeprintui-devel >= 2.4.2
#BuildRequires:	mono-devel
BuildRequires:	libgda2.0-devel >= 3.1.1
BuildRequires:	gnome-db2.0-devel >= 3.0.1
BuildRequires:	libpx-devel >= 0.3.0
BuildRequires:	libpsiconv-devel
BuildRequires:	pygtk2.0-devel
BuildRequires:	perl-devel
BuildRequires:  scrollkeeper
BuildRequires:  intltool
#BuildRequires:	guile-devel >= 1.6
BuildRequires:  automake1.7
BuildRequires:  desktop-file-utils
Requires:	pygtk2.0
Requires: goffice >= %goffice
Requires(post):	scrollkeeper >= 0.3
Requires(postun):	scrollkeeper >= 0.3

%description
This is the Gnumeric, the GNOME spreadsheet program. If you are familiar with 
Excel, you should be ready to use Gnumeric.  It tries to clone all of 
the good features and stay as compatible as possible with Excel in terms of 
usability. Hopefully the bugs have been left behind :).


%package -n %libname
Summary: Spreadsheet library from Gnumeric
Group: System/Libraries

%description -n %libname
This is the Gnumeric, the GNOME spreadsheet program. If you are familiar with 
Excel, you should be ready to use Gnumeric.  It tries to clone all of 
the good features and stay as compatible as possible with Excel in terms of 
usability. Hopefully the bugs have been left behind :).

%package -n %develname
Summary: Spreadsheet library from Gnumeric - development files
Group: Development/C
Requires: %libname = %version
Provides: libspreadsheet-devel = %version-%release
Provides: %{name}-devel = %version-%release
Obsoletes: %{name}-devel


%description -n %develname
This is the Gnumeric, the GNOME spreadsheet program. If you are familiar with 
Excel, you should be ready to use Gnumeric.  It tries to clone all of 
the good features and stay as compatible as possible with Excel in terms of 
usability. Hopefully the bugs have been left behind :).


%prep
%setup -q
%patch -p1
%patch1 -p1
%patch3 -p1

%build

%configure2_5x --enable-ssindex

%make

%install
rm -rf $RPM_BUILD_ROOT %{name}.lang
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
rm -vf %buildroot%_datadir/%name/%version/perl/*/auto/Gnumeric/.packlist
rm -rf %buildroot/var
ln -s %_datadir/gnome %buildroot%_datadir/%name/%version

find %buildroot -name \*.la|xargs chmod 644

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="Science" \
  --remove-category="Math" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="GNOME" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# icon
mkdir -p $RPM_BUILD_ROOT%{_liconsdir}
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}
mkdir -p $RPM_BUILD_ROOT%{_miconsdir}
cp -f %{SOURCE2} $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
cp -f %{SOURCE3} $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
cp -f %{SOURCE4} $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png

%find_lang %{name} --with-gnome
%find_lang %{name}-functions
cat %name-functions.lang >> %name.lang

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}
%update_scrollkeeper
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
for schema in gnumeric-dialogs gnumeric-general gnumeric-plugins; do 
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$schema.schemas > /dev/null
done

%preun
if [ "$1" = "0" ]; then
 export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
 for schema in gnumeric-dialogs gnumeric-general gnumeric-plugins; do 
   gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/$schema.schemas > /dev/null
 done
fi

%postun
%{clean_menus}
%clean_scrollkeeper

%post -n %libname -p /sbin/ldconfig 
%postun -n %libname -p /sbin/ldconfig 

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS NEWS BUGS README
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%{_libdir}/gnumeric
%{_datadir}/gnumeric
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_mandir}/man1/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%dir %{_datadir}/omf/gnumeric
%{_datadir}/omf/gnumeric/gnumeric-C.omf

%files -n %libname
%defattr(-, root, root)
%_libdir/libspreadsheet-%version.so

%files -n %develname
%defattr(-, root, root)
%_libdir/libspreadsheet.so
%_libdir/lib*.la
%_libdir/pkgconfig/*.pc
%_includedir/libspreadsheet-*/


