function [ version ] = GetLibraryVersion ( )
%GetLibraryVersion : Returns dll version

if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return
end

version = calllib ('XPS_Q8_drivers', 'GetLibraryVersion') ;
