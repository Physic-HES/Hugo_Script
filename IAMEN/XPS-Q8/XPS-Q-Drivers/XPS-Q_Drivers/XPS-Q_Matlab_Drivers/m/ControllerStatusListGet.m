function [errorCode, ControllerStatusList] = ControllerStatusListGet(socketId)
%ControllerStatusListGet :  Controller status list
%
%	[errorCode, ControllerStatusList] = ControllerStatusListGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		cstring ControllerStatusList


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
ControllerStatusList = '';
for i = 1:103
	ControllerStatusList = [ControllerStatusList '          '];
end

% lib call
[errorCode, ControllerStatusList] = calllib('XPS_Q8_drivers', 'ControllerStatusListGet', socketId, ControllerStatusList);
