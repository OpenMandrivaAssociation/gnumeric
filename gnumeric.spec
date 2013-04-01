%define url_ver %(echo %{version}|cut -d. -f1,2)

%define goffice 0.10
%define libname %mklibname spreadsheet %{version}
%define devname %mklibname -d spreadsheet

Summary:	A full-featured spreadsheet for GNOME
Name:		gnumeric
Version:	1.12.1
Release:	1
License:	GPLv2+
Group:		Office
URL:		http://www.gnome.org/projects/gnumeric/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
#This patch is borked, leave it here as reference
# configure is disabling gda for now
Patch1:		gnumeric-1.9.17-format-strings.patch
# (fc) 1.9.3-4mdv fix CVE-2009-0318
Patch5:		gnumeric-1.8.2-CVE-2009-0318-rh.patch

BuildRequires:	desktop-file-utils
BuildRequires:	intltool
BuildRequires:	rarian
BuildRequires:	perl-devel
BuildRequires:	psiconv-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libgda-5.0)
BuildRequires:	pkgconfig(libgoffice-0.10)
BuildRequires:	pkgconfig(libgsf-1)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(pxlib)
BuildRequires:	pkgconfig(pygobject-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	perl-IO-Compress

Requires:	pygtk2.0
#gw it places files in the versioned goffice directory
# But as usual with the G mess, stuff doesn't make sense and
# goffice's version is 0.9 while its filesystem version is
# 0.10...
Requires: goffice >= 0.9

%description
This is the Gnumeric, the GNOME spreadsheet program. If you are familiar with 
Excel, you should be ready to use Gnumeric.  It tries to clone all of 
the good features and stay as compatible as possible with Excel in terms of 
usability. Hopefully the bugs have been left behind :).


%package -n %{libname}
Summary:	Spreadsheet library from Gnumeric
Group:		System/Libraries

%description -n %{libname}
This is the Gnumeric, the GNOME spreadsheet program. If you are familiar with 
Excel, you should be ready to use Gnumeric.  It tries to clone all of 
the good features and stay as compatible as possible with Excel in terms of 
usability. Hopefully the bugs have been left behind :).

%package -n %{devname}
Summary:	Spreadsheet library from Gnumeric - development files
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libspreadsheet-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel

%description -n %{devname}
This is the Gnumeric, the GNOME spreadsheet program. If you are familiar with 
Excel, you should be ready to use Gnumeric.  It tries to clone all of 
the good features and stay as compatible as possible with Excel in terms of 
usability. Hopefully the bugs have been left behind :).

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--enable-ssindex

%make

%install
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
rm -vf %{buildroot}%_datadir/%{name}/%{version}/perl/*/auto/Gnumeric/.packlist
rm -rf %{buildroot}/var
ln -s %_datadir/gnome %{buildroot}%_datadir/%{name}/%{version}

find %{buildroot} -name \*.la|xargs chmod 644

desktop-file-install --vendor="" \
	--remove-category="Application" \
	--remove-category="Science" \
	--remove-category="Math" \
	--remove-category="Application" \
	--remove-mime-type="zz-application/zz-winassoc-xls" \
	--add-category="GTK" \
	--add-category="GNOME" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

%find_lang %{name} --with-gnome
%find_lang %{name}-functions
cat %{name}-functions.lang >> %{name}.lang

%preun
%preun_uninstall_gconf_schemas %schemas

%files -f %{name}.lang
%doc AUTHORS NEWS BUGS README
%{_bindir}/*
%{_libdir}/goffice/%goffice/plugins/gnumeric
%{_libdir}/gnumeric
%{_datadir}/glib-2.0/schemas/org.gnome.gnumeric*.xml
%{_datadir}/gnumeric
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_iconsdir}/hicolor/*/apps/gnumeric*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libspreadsheet-%{version}.so

%files -n %{devname}
%{_libdir}/libspreadsheet.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libspreadsheet-*/

