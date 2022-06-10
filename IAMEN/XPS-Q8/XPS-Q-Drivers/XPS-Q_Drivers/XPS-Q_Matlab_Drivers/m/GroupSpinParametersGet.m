function [errorCode, Velocity, Acceleration] = GroupSpinParametersGet(socketId, GroupName)
%GroupSpinParametersGet :  Get Spin parameters on selected group
%
%	[errorCode, Velocity, Acceleration] = GroupSpinParametersGet(socketId, GroupName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%	* Output parameters :
%		int32 errorCode
%		doublePtr Velocity
%		doublePtr Acceleration


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
Velocity = 0;
Acceleration = 0;

% lib call
[errorCode, GroupName, Velocity, Acceleration] = calllib('XPS_Q8_drivers', 'GroupSpinParametersGet', socketId, GroupName, Velocity, Acceleration);
