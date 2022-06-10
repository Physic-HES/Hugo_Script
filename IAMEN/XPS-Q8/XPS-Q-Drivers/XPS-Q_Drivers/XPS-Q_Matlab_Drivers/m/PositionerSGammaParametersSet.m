function [errorCode] = PositionerSGammaParametersSet(socketId, PositionerName, Velocity, Acceleration, MinimumTjerkTime, MaximumTjerkTime)
%PositionerSGammaParametersSet :  Update dynamic parameters for one axe of a group for a future displacement
%
%	[errorCode] = PositionerSGammaParametersSet(socketId, PositionerName, Velocity, Acceleration, MinimumTjerkTime, MaximumTjerkTime)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double Velocity
%		double Acceleration
%		double MinimumTjerkTime
%		double MaximumTjerkTime
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerSGammaParametersSet', socketId, PositionerName, Velocity, Acceleration, MinimumTjerkTime, MaximumTjerkTime);
