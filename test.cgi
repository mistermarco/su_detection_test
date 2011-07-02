#!/usr/bin/perl
use strict;
use CGI;
use LWP::UserAgent;
use HTTP::Cookies;
use Test::More;

my $q = new CGI;
print $q->header;

# turn off output buffering
$|++;

my $test_url = 'http://www.stanford.edu/~mrmarco/cgi-bin/mobile/test/index.cgi';
my $tests_file = 'mobile_ua_strings.txt';
my $cookie_domain = '.stanford.edu';
my $cookie_name   = 'COOKIE_DEVICE_CLASS';
my $cookie_path   = '/';

#
# create a new user agent
#

my $ua = LWP::UserAgent->new(timeout => 10);

#
# create a new cookie jar to store cookies as we get them
#

my $cookie_jar = HTTP::Cookies->new(autosave => 1);
$ua->cookie_jar($cookie_jar);

#
# load the tests
#

open (FILE, $tests_file) or die ("Unable to open file $tests_file");
my @tests = <FILE>;
my $number_of_tests = (scalar @tests) * 2; # doubled because we run two tests per line
close(FILE);

# 
# perform the tests
#

foreach (@tests) {
  # remove the end of line character
  chomp;

  # UA string and expected device class are separated by a tab
  my ($ua_string, $class) = split("\t");

  # set the user agent string
  $ua->agent($ua_string);

  # connect to the test URL
  my $response = $ua->get($test_url);

  # the only thing the test script returns is the value of the environment variable
  my $environment_variable = $response->decoded_content;

  # the cookie is returned by Apache and should be stored by the LWP user agent
  my $cookie_value         = $cookie_jar->{'COOKIES'}{$cookie_domain}{$cookie_path}{$cookie_name}[1];

  # test that the cookie value and the environment variable values are the same
  is($cookie_value,$environment_variable, "values match ($cookie_value:$environment_variable) for $ua_string");

  # test that the cookie value is the same as the expected class 
  is($cookie_value,$class, "$class: $ua_string" );

  # clear the cookie jar so that previous responses don't poison later ones
  $cookie_jar->clear;
}

done_testing($number_of_tests);
