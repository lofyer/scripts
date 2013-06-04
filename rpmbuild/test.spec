Name:           greet
Version:       	1.0
Release:        1%{?dist}
Summary:        Greets the invoker

Group:         	Greetings Group
License:        GPL
URL:         	 http://www.sgniteerg.com
Source0:        greet.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description

%prep
%setup -q
%build
%install
install -m 0755 -d $RPM_BUILD_ROOT/opt/greet
install -m 0777 greet.sh $RPM_BUILD_ROOT/opt/greet/greet.sh

%clean
#rm -rf $RPM_BUILD_ROOT

%files
%dir /opt/greet
/opt/greet/greet.sh

%defattr(-,root,root,-)
%doc
%changelog
