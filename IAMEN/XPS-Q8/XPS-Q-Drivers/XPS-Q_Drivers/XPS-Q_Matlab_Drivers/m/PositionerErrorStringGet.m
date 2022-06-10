function [errorCode, PositionerErrorString] = PositionerErrorStringGet(socketId, PositionerErrorCode)
%PositionerErrorStringGet :  Return the positioner status string corresponding to the positioner error code
%
%	[errorCode, PositionerErrorString] = PositionerErrorStringGet(socketId, PositionerErrorCode)
%
%	* Input parameters :
%		int32 socketId
%		int32 PositionerErrorCode
%	* Output parameters :
%		int32 errorCode
%		cstring PositionerErrorString


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
PositionerErrorString = '';
for i = 1:103
	PositionerErrorString = [PositionerErrorString '          '];
end

% lib call
[errorCode, PositionerErrorString] = calllib('XPS_Q8_drivers', 'PositionerErrorStringGet', socketId, PositionerErrorCode, PositionerErrorString);
