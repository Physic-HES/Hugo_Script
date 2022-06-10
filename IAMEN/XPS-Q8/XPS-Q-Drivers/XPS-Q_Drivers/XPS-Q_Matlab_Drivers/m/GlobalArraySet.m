function [errorCode] = GlobalArraySet(socketId, Number, ValueString)
%GlobalArraySet :  Set global array value
%
%	[errorCode] = GlobalArraySet(socketId, Number, ValueString)
%
%	* Input parameters :
%		int32 socketId
%		int32 Number
%		cstring ValueString
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, ValueString] = calllib('XPS_Q8_drivers', 'GlobalArraySet', socketId, Number, ValueString);
