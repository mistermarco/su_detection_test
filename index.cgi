#!/usr/bin/perl
use CGI;
use strict;
my $q = new CGI;
print $q->header;
print $ENV{'HTTP_DEVICE_CLASS'};
