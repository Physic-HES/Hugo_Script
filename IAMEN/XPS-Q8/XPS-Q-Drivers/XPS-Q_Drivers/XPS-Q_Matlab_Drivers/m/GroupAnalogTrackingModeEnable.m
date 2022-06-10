function [errorCode] = GroupAnalogTrackingModeEnable(socketId, GroupName, Type)
%GroupAnalogTrackingModeEnable :  Enable Analog Tracking mode on selected group
%
%	[errorCode] = GroupAnalogTrackingModeEnable(socketId, GroupName, Type)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		cstring Type
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName, Type] = calllib('XPS_Q8_drivers', 'GroupAnalogTrackingModeEnable', socketId, GroupName, Type);
