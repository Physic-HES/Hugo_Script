function [errorCode, PositionerDriverStatusList] = PositionerDriverStatusListGet(socketId)
%PositionerDriverStatusListGet :  Positioner driver status list
%
%	[errorCode, PositionerDriverStatusList] = PositionerDriverStatusListGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring PositionerDriverStatusList


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
PositionerDriverStatusList = '';
for i = 1:205
	PositionerDriverStatusList = [PositionerDriverStatusList '          '];
end

% lib call
[errorCode, PositionerDriverStatusList] = calllib('XPS_Q8_drivers', 'PositionerDriverStatusListGet', socketId, PositionerDriverStatusList);
