#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# pytest tests

Summary:	A tool to convert TrueType/OpenType fonts to XML and back
Summary(pl.UTF-8):	Narzędzie do konwersji fontów TrueType/OpenType do/z XML-a
Name:		fonttools
Version:	4.60.1
Release:	1
# basic license is BSD
# FontTools includes Adobe AGL & AGLFN, which is under 3-clauses BSD license
License:	MIT, BSD
Group:		Development/Tools
#Source0Download: https://github.com/fonttools/fonttools/releases
Source0:	https://github.com/fonttools/fonttools/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9953a8262cac55018d110edeb7ef2981
URL:		https://github.com/fonttools/fonttools
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	python3-Cython
BuildRequires:	python3-devel >= 1:3.9
%if %{with tests}
BuildRequires:	python3-brotli >= 1.0.9
#BuildRequires:	python3-freetype-py >= 2.3.0
BuildRequires:	python3-fs >= 2.4.16
BuildRequires:	python3-fs < 3
BuildRequires:	python3-lxml >= 4
BuildRequires:	python3-lz4 >= 1.7.4.2
BuildRequires:	python3-matplotlib
BuildRequires:	python3-pycairo
BuildRequires:	python3-pytest >= 7.0.0
# >= 1.9.1?
BuildRequires:	python3-scipy >= 1.7.3
BuildRequires:	python3-skia-pathops >= 0.7.2
BuildRequires:	python3-sympy
#BuildRequires:	python3-ufoLib2 >= 0.13.1
#BuildRequires:	python3-uharfbuzz >= 0.30.0
%if "%{_ver_lt %{py3_ver} 3.12}" == "1"
BuildRequires:	python3-unicodedata2 >= 15.1.0
%endif
BuildRequires:	python3-zopfli >= 0.2.1
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.750
%if %{with doc}
#BuildRequires:	python3-freetype-py >= 2.5.1
BuildRequires:	python3-reportlab >= 4.2.5
BuildRequires:	python3-sphinx_rtd_theme >= 3.0.2
BuildRequires:	sphinx-pdg-3 >= 8.1.3
%endif
Requires:	python3-fonttools = %{version}-%{release}
Requires:	python3-setuptools
Provides:	ttx = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TTX/FontTools is a tool for manipulating TrueType and OpenType fonts.
It is written in Python and has a BSD-style, open-source license. TTX
can dump TrueType and OpenType fonts to an XML-based text format and
vice versa.

%description -l pl.UTF-8
TTX/FontTools to narzędzie do operacji na fontach TrueType i OpenType.
Zostało napisane w Pythonie i ma otwartą licencję w stylu BSD. TTX
potrafi wykonywać zrzuty fontów TrueType i OpenType do formatu
tekstowego opartego na XML-u oraz dokonać operacji odwrotnej.

%package -n python3-fonttools
Summary:	Python 3 tools to manipulate font files
Summary(pl.UTF-8):	Narzędzia do manipulacji na plikach fontów dla Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.9
%if "%{_ver_lt %{py3_ver} 3.12}" == "1"
Requires:	python3-unicodedata2 >= 15.1.0
%endif

%description -n python3-fonttools
Python 3 tools to manipulate font files.

%description -n python3-fonttools -l pl.UTF-8
Narzędzia do manipulacji na plikach fontów dla Pythona 3.

%package -n python3-fonttools-apidocs
Summary:	Documentation for Python fonttools module
Summary(pl.UTF-8):	Dokumentacja modułu Pythona fonttools
Group:		Documentation
BuildArch:	noarch

%description -n python3-fonttools-apidocs
Documentation for Python fonttools module.

%description -n python3-fonttools-apidocs -l pl.UTF-8
Dokumentacja modułu Pythona fonttools.

%prep
%setup -q

%build
%py3_build

%if %{with tests}
PATH="$(pwd):$PATH" \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/Lib \
%{__python3} -m pytest Tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/Lib \
%{__make} -C Doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

# sources
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/fontTools/*u2*u/*.c

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE LICENSE.external NEWS.rst README.rst SECURITY.md
%attr(755,root,root) %{_bindir}/fonttools
%attr(755,root,root) %{_bindir}/pyftmerge
%attr(755,root,root) %{_bindir}/pyftsubset
%attr(755,root,root) %{_bindir}/ttx
%{_mandir}/man1/ttx.1*

%files -n python3-fonttools
%defattr(644,root,root,755)
%dir %{py3_sitedir}/fontTools
%{py3_sitedir}/fontTools/*.py
%{py3_sitedir}/fontTools/__pycache__
%{py3_sitedir}/fontTools/cffLib
%{py3_sitedir}/fontTools/colorLib
%{py3_sitedir}/fontTools/config
%dir %{py3_sitedir}/fontTools/cu2qu
%attr(755,root,root) %{py3_sitedir}/fontTools/cu2qu/cu2qu.cpython-*.so
%{py3_sitedir}/fontTools/cu2qu/*.py
%{py3_sitedir}/fontTools/cu2qu/__pycache__
%{py3_sitedir}/fontTools/designspaceLib
%{py3_sitedir}/fontTools/encodings
%{py3_sitedir}/fontTools/feaLib
%{py3_sitedir}/fontTools/merge
%{py3_sitedir}/fontTools/misc
%{py3_sitedir}/fontTools/mtiLib
%{py3_sitedir}/fontTools/otlLib
%{py3_sitedir}/fontTools/pens
%dir %{py3_sitedir}/fontTools/qu2cu
%attr(755,root,root) %{py3_sitedir}/fontTools/qu2cu/qu2cu.cpython-*.so
%{py3_sitedir}/fontTools/qu2cu/*.py
%{py3_sitedir}/fontTools/qu2cu/__pycache__
%{py3_sitedir}/fontTools/subset
%{py3_sitedir}/fontTools/svgLib
%{py3_sitedir}/fontTools/t1Lib
%{py3_sitedir}/fontTools/ttLib
%{py3_sitedir}/fontTools/ufoLib
%{py3_sitedir}/fontTools/unicodedata
%{py3_sitedir}/fontTools/varLib
%{py3_sitedir}/fontTools/voltLib
%{py3_sitedir}/fonttools-%{version}-py*.egg-info

%if %{with doc}
%files -n python3-fonttools-apidocs
%defattr(644,root,root,755)
%doc Doc/build/html/{_images,_modules,_static,cffLib,colorLib,cu2qu,designspaceLib,encodings,feaLib,misc,otlLib,pens,qu2cu,subset,svgLib,ttLib,ufoLib,unicodedata,varLib,voltLib,*.html,*.js}
%endif
