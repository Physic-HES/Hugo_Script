function [errorCode] = GroupSpinParametersSet(socketId, GroupName, Velocity, Acceleration)
%GroupSpinParametersSet :  Modify Spin parameters on selected group and activate the continuous move
%
%	[errorCode] = GroupSpinParametersSet(socketId, GroupName, Velocity, Acceleration)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		double Velocity
%		double Acceleration
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName] = calllib('XPS_Q8_drivers', 'GroupSpinParametersSet', socketId, GroupName, Velocity, Acceleration);
