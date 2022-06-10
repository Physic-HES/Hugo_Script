function [errorCode] = GroupSpinModeStop(socketId, GroupName, Acceleration)
%GroupSpinModeStop :  Stop Spin mode on selected group with specified acceleration
%
%	[errorCode] = GroupSpinModeStop(socketId, GroupName, Acceleration)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		double Acceleration
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName] = calllib('XPS_Q8_drivers', 'GroupSpinModeStop', socketId, GroupName, Acceleration);
