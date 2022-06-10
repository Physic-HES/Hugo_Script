function [errorCode, ValueString] = GlobalArrayGet(socketId, Number)
%GlobalArrayGet :  Get global array value
%
%	[errorCode, ValueString] = GlobalArrayGet(socketId, Number)
%
%	* Input parameters :
%		int32 socketId
%		int32 Number
%	* Output parameters :
%		int32 errorCode
%		cstring ValueString


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
ValueString = '';
for i = 1:103
	ValueString = [ValueString '          '];
end

% lib call
[errorCode, ValueString] = calllib('XPS_Q8_drivers', 'GlobalArrayGet', socketId, Number, ValueString);
