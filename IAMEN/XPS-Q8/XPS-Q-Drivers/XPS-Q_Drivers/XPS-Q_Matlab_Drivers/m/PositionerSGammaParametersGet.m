function [errorCode, Velocity, Acceleration, MinimumTjerkTime, MaximumTjerkTime] = PositionerSGammaParametersGet(socketId, PositionerName)
%PositionerSGammaParametersGet :  Read dynamic parameters for one axe of a group for a future displacement 
%
%	[errorCode, Velocity, Acceleration, MinimumTjerkTime, MaximumTjerkTime] = PositionerSGammaParametersGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr Velocity
%		doublePtr Acceleration
%		doublePtr MinimumTjerkTime
%		doublePtr MaximumTjerkTime


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
Velocity = 0;
Acceleration = 0;
MinimumTjerkTime = 0;
MaximumTjerkTime = 0;

% lib call
[errorCode, PositionerName, Velocity, Acceleration, MinimumTjerkTime, MaximumTjerkTime] = calllib('XPS_Q8_drivers', 'PositionerSGammaParametersGet', socketId, PositionerName, Velocity, Acceleration, MinimumTjerkTime, MaximumTjerkTime);
