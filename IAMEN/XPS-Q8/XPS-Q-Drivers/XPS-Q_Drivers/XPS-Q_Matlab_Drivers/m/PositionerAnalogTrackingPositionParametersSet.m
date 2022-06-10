function [errorCode] = PositionerAnalogTrackingPositionParametersSet(socketId, PositionerName, GPIOName, Offset, Scale, Velocity, Acceleration)
%PositionerAnalogTrackingPositionParametersSet :  Update dynamic parameters for one axe of a group for a future analog tracking position
%
%	[errorCode] = PositionerAnalogTrackingPositionParametersSet(socketId, PositionerName, GPIOName, Offset, Scale, Velocity, Acceleration)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		cstring GPIOName
%		double Offset
%		double Scale
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
[errorCode, PositionerName, GPIOName] = calllib('XPS_Q8_drivers', 'PositionerAnalogTrackingPositionParametersSet', socketId, PositionerName, GPIOName, Offset, Scale, Velocity, Acceleration);
