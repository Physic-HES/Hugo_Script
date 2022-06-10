function [errorCode, PositionerErrorList] = PositionerErrorListGet(socketId)
%PositionerErrorListGet :  Positioner error list
%
%	[errorCode, PositionerErrorList] = PositionerErrorListGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring PositionerErrorList


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
PositionerErrorList = '';
for i = 1:205
	PositionerErrorList = [PositionerErrorList '          '];
end

% lib call
[errorCode, PositionerErrorList] = calllib('XPS_Q8_drivers', 'PositionerErrorListGet', socketId, PositionerErrorList);
