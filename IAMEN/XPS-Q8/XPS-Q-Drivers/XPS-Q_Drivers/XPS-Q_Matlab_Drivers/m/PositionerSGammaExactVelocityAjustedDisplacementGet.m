function [errorCode, AdjustedDisplacement] = PositionerSGammaExactVelocityAjustedDisplacementGet(socketId, PositionerName, DesiredDisplacement)
%PositionerSGammaExactVelocityAjustedDisplacementGet :  Return adjusted displacement to get exact velocity
%
%	[errorCode, AdjustedDisplacement] = PositionerSGammaExactVelocityAjustedDisplacementGet(socketId, PositionerName, DesiredDisplacement)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double DesiredDisplacement
%	* Output parameters :
%		int32 errorCode
%		doublePtr AdjustedDisplacement


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
AdjustedDisplacement = 0;

% lib call
[errorCode, PositionerName, AdjustedDisplacement] = calllib('XPS_Q8_drivers', 'PositionerSGammaExactVelocityAjustedDisplacementGet', socketId, PositionerName, DesiredDisplacement, AdjustedDisplacement);
