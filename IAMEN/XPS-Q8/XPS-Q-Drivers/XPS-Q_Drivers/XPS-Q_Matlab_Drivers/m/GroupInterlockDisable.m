function [errorCode] = GroupInterlockDisable(socketId, GroupName)
%GroupInterlockDisable :  Set group interlock disable
%
%	[errorCode] = GroupInterlockDisable(socketId, GroupName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName] = calllib('XPS_C8_drivers', 'GroupInterlockDisable', socketId, GroupName);
