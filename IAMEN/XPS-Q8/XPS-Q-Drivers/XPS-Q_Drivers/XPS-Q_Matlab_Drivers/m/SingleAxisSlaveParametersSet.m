function [errorCode] = SingleAxisSlaveParametersSet(socketId, GroupName, PositionerName, Ratio)
%SingleAxisSlaveParametersSet :  Set slave parameters
%
%	[errorCode] = SingleAxisSlaveParametersSet(socketId, GroupName, PositionerName, Ratio)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		cstring PositionerName
%		double Ratio
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName, PositionerName] = calllib('XPS_Q8_drivers', 'SingleAxisSlaveParametersSet', socketId, GroupName, PositionerName, Ratio);
