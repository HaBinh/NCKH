#!/usr/bin/perl -w

# kevin lenzo 12/07
#
# run the decision tree letter-to-phone rules
# 
# if run with no arguments, goes into interactive
# mode.  If given an argument, it expects the arg
# to be a t2p dictionary alignment, from which it
# will generate statistics.




# set the decision tree to use in the next line here.
# it will load the subroutine.
$interact = (!@ARGV);

if ($interact) {
    print "\nplease input an argument\n";
    exit;
}else{
	require "cmd_r1d7.pl"; # the big tree from the 58K dictionary
    #lấy argument nhập từ command line
	$argument=$ARGV[0];
	my @phones;
    
	foreach $word (split /\s+/, $argument) {
	    push @phones, &l2p(split(//, $word));
	}
	{
   	no warnings 'once';
   	$phones = join(" ", &cleanup(@phones));
	}
	
	my $phones .= join(" ", @phones);
	$chuoiamvi= join(" ", @phones)."\n";

    

    print $chuoiamvi;
	
}


sub cleanup {
    # clean up the phonetic output a little

    my @phones = @_;
    my $x = " ".join(" ", @phones)." ";

    $x =~ s/ (\S+)( \1)+/ $1/g;
    $x =~ s/N NG/NG/g;

    $x =~ s/[AEIOU]X?[^R] ([AEIOU]X?R)/$1/g;

    $x =~ s/_//g;
    $x =~ s/^\s+//;
    $x =~ s/\s+$//;
    $x =~ s/\s+/ /g;

    split(/\s+/, $x);
}


sub l2p {
    # the letter-to-phone workhorse
    my @letters = @_;

    my @orig_letter = @letters;
    push @letters, ('-', '-', '-');
    unshift @letters, ('-', '-', '-');

    my @result; 
    my $localgoodcount = 0;
    my $opos;
    my @phones;

    for $opos (0..$#orig_letter) {
	# context2phone is the dtree subroutine from the "require"
	$res = &context2phone(@letters[$opos..$opos+6]);
	push @phones, $res;
    }

    @phones;
}
