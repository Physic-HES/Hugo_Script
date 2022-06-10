function [errorCode, PositionerHardwareStatusList] = PositionerHardwareStatusListGet(socketId)
%PositionerHardwareStatusListGet :  Positioner hardware status list
%
%	[errorCode, PositionerHardwareStatusList] = PositionerHardwareStatusListGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring PositionerHardwareStatusList


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
PositionerHardwareStatusList = '';
for i = 1:205
	PositionerHardwareStatusList = [PositionerHardwareStatusList '          '];
end

% lib call
[errorCode, PositionerHardwareStatusList] = calllib('XPS_Q8_drivers', 'PositionerHardwareStatusListGet', socketId, PositionerHardwareStatusList);
