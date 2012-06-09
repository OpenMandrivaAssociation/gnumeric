%define libname %mklibname spreadsheet %version
%define develname %mklibname -d spreadsheet
%define goffice 0.10

Name: gnumeric
Summary: A full-featured spreadsheet for GNOME
Version: 1.11.3
Release: 3
License: GPLv2+
Group: Office
Source0: http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz
Source2: %{name}-32.png
Source3: %{name}-16.png
Source4: %{name}-48.png
#This patch is borked, leave it here as reference
# configure is disabling gda for now
Patch0:	gnumeric-1.11.3-gda-build.patch
Patch1: gnumeric-1.9.17-format-strings.patch
# (fc) 1.9.3-4mdv fix CVE-2009-0318
Patch5: gnumeric-1.8.2-CVE-2009-0318-rh.patch
URL:http://www.gnome.org/projects/gnumeric/

Requires: %libname = %version
BuildRequires: pkgconfig(glib-2.0) >= 2.28.0
BuildRequires: pkgconfig(gmodule-2.0) >= 2.28.0
BuildRequires: pkgconfig(gobject-2.0) >= 2.28.0
BuildRequires: pkgconfig(gthread-2.0) >= 2.28.0
BuildRequires: pkgconfig(gtk+-3.0) >= 3.0.0
BuildRequires: pkgconfig(libgda-4.0) >= 4.1.1
BuildRequires: pkgconfig(libgoffice-0.10) >= 0.9.2
BuildRequires: pkgconfig(libgsf-1) >= 1.14.18
BuildRequires: pkgconfig(libxml-2.0) >= 2.4.12
BuildRequires: pkgconfig(pango) >= 1.24.0
BuildRequires: pkgconfig(pangocairo) >= 1.24.0
BuildRequires: pkgconfig(pxlib) >= 0.4.0
BuildRequires: pkgconfig(pygobject-2.0) >= 2.12.0
BuildRequires:  gtk+2-devel
BuildRequires:	psiconv-devel
BuildRequires:	perl-devel
BuildRequires:  scrollkeeper
BuildRequires:  intltool
#BuildRequires:	guile-devel >= 1.6
BuildRequires:  desktop-file-utils
Requires:	pygtk2.0
#gw it places files in the versioned goffice directory
# But as usual with the G mess, stuff doesn't make sense and
# goffice's version is 0.9 while its filesystem version is
# 0.10...
Requires: goffice >= 0.9
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
%apply_patches

%build
autoreconf -fi
%configure2_5x --enable-ssindex
%make

%install
rm -rf %{buildroot} %{name}.lang
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
  --remove-mime-type="zz-application/zz-winassoc-xls" \
  --add-category="GTK" \
  --add-category="GNOME" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# icon
mkdir -p %{buildroot}%{_liconsdir}
mkdir -p %{buildroot}%{_iconsdir}
mkdir -p %{buildroot}%{_miconsdir}
cp -f %{SOURCE2} %{buildroot}/%{_iconsdir}/%{name}.png
cp -f %{SOURCE3} %{buildroot}/%{_miconsdir}/%{name}.png
cp -f %{SOURCE4} %{buildroot}/%{_liconsdir}/%{name}.png

%find_lang %{name} --with-gnome
%find_lang %{name}-functions
cat %name-functions.lang >> %name.lang

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%update_scrollkeeper
%define schemas gnumeric-dialogs gnumeric-general gnumeric-plugins
%post_install_gconf_schemas %schemas
%update_icon_cache hicolor
%endif

%preun
%preun_uninstall_gconf_schemas %schemas

%if %mdkversion < 200900
%postun
%clean_icon_cache hicolor
%{clean_menus}
%clean_scrollkeeper

%post -n %libname -p /sbin/ldconfig 
%postun -n %libname -p /sbin/ldconfig 
%endif

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS NEWS BUGS README
%{_bindir}/*
%{_libdir}/goffice/%goffice/plugins/gnumeric
%{_libdir}/gnumeric
%{_datadir}/gnumeric
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%_datadir/icons/hicolor/*/apps/gnumeric*
%{_mandir}/man1/*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/glib-2.0/schemas/org.gnome.gnumeric*.xml

%files -n %libname
%defattr(-, root, root)
%_libdir/libspreadsheet-%version.so

%files -n %develname
%defattr(-, root, root)
%_libdir/libspreadsheet.so
%_libdir/pkgconfig/*.pc
%_includedir/libspreadsheet-*/

