function [errorCode] = SingleAxisThetaSlaveParametersSet(socketId, GroupName, PositionerName, Ratio)
%SingleAxisThetaSlaveParametersSet :  Set slave parameters
%
%	[errorCode] = SingleAxisThetaSlaveParametersSet(socketId, GroupName, PositionerName, Ratio)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		cstring PositionerName
%		double Ratio
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName, PositionerName] = calllib('XPS_C8_drivers', 'SingleAxisThetaSlaveParametersSet', socketId, GroupName, PositionerName, Ratio);
